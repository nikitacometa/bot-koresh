import logging
from datetime import datetime, timedelta, timezone
from time import sleep
from typing import List, Optional

from telegram import Update, Message, User
from telegram.ext import CallbackContext

from koresh.bot.commands.admin_mode import is_admin, try_process_admin_command
from koresh.bot.commands.create_challenge import create_challenge
from koresh.bot.commands.show_map import extract_coordinates
from koresh.bot.commands.troll_mode import is_troll
from koresh.utils.classes.decorators import moshnar_command
from koresh.bot.commands.delete_after import delete_after_f
from koresh.bot.commands.save_photo import save_photo
from koresh.bot.commands.split_teams import split_into_teams
from koresh.bot.context import app_context
from koresh.bot.settings import BOT_CHAT_ID
from koresh.bot.validator import is_valid_bitcoin_address
from koresh.managers.phrase_manager import PhraseManager
from koresh.utils.message_utils import send_sladko


# TODO: make parse_utils or Parser
from koresh.utils.parse_utils import get_alpha_part
from koresh.utils.str_utils import parse_time_to_seconds


def have_start_in_list(tokens: List[str], starts: List[str]) -> bool:
    return any(filter(lambda token: any(filter(lambda s: token.startswith(s), starts)), tokens))


def have_inside_in_list(tokens: List[str], starts: List[str]) -> bool:
    return any(filter(lambda token: any(filter(lambda s: s in token, starts)), tokens))


def have_starts(tokens: List[str], *args):
    return have_start_in_list(tokens, [arg for arg in args])


def have_inside(tokens: List[str], *args):
    return have_inside_in_list(tokens, [arg for arg in args])


def has_mention_of_me(tokens: List[str]) -> bool:
    return have_start_in_list(tokens, ['кореш', 'корефан']) and not have_start_in_list(tokens, ['корешами'])


def is_reply_to_me(message: Message):
    try:
        return message.reply_to_message.from_user.id == app_context.bot.id
    except Exception:
        return False


def is_thanks(tokens: List[str]) -> bool:
    return are_in_a_row(tokens, ['от', 'души']) or have_start_in_list(tokens, ['спс', 'сяп', 'спасиб', 'сенкс'])


def are_in_a_row(tokens: List[str], words: List[str]) -> bool:
    if len(words) > len(tokens):
        return False

    # TODO: optimize
    for i in range(len(tokens) - len(words) + 1):
        ok = True
        for j in range(len(words)):
            if not tokens[j + i].startswith(words[j]):
                ok = False
                break
        if ok:
            return True
    return False


def is_my_chat(update: Update) -> bool:
    return update.message.chat.id == BOT_CHAT_ID


def is_split_request(tokens: List[str]) -> bool:
    return have_start_in_list(tokens, ['подели', 'намошни', 'раздели', 'посплить']) and \
           have_start_in_list(tokens, ['плиз', 'плз', 'плез', 'пож', 'по-братски'])


def is_question(tokens: List[str]) -> bool:
    return '?' in tokens[-1]


def get_delete_after(tokens: List[str]) -> Optional[str]:
    option = list(filter(lambda token: token.startswith('$') and token[-1] in 'smhd', tokens))
    return option[0] if len(option) > 0 else None


def is_sladko(msg: Message) -> bool:
    if msg.sticker is None:
        return False

    return msg.sticker.file_unique_id == 'AgADBgADhlyiAw'


@moshnar_command
def default_message_handler(update: Update, context: CallbackContext):
    logging.debug('default handler')

    if try_process_admin_command(update, context):
        return

    message: Message = update.message
    sender: User = message.from_user
    text: str = message.text
    tokens = text.split() if text is not None else []
    low_tokens = text.lower().split() if text is not None else []

    try:
        coords = extract_coordinates(tokens)
        if coords:
            img_link = app_context.map_client.get_img_link_by_coordinates(coords)
            update.message.reply_photo(photo=img_link)
    except Exception as e:
        logging.exception(e)

    # TODO: reformat for easy creating of new situations/cases
    for s in tokens:
        try:
            alpha_part = get_alpha_part(s)
            if is_valid_bitcoin_address(alpha_part):
                try:
                    app_context.tracking_manager.track_address(alpha_part, message, context.bot)
                except Exception as e:
                    logging.exception(e)
            return
        except Exception:
            pass

    if sender.first_name in ['Mark', 'Марк']:
        # TODO: store this info in DB
        last_hi_o = context.bot_data.get('last_hi_mark', None)
        if not last_hi_o or datetime.now(timezone.utc) - last_hi_o > timedelta(seconds=1):
            reply = message.reply_text('ooh hi Mark)')
            context.bot_data['last_hi_mark'] = reply.date

    last_msgs = context.chat_data['last_msgs']
    if len(last_msgs) >= 2 and is_sladko(last_msgs[-1]) and is_sladko(last_msgs[-2]):
        send_sladko(context.bot, message.chat.id)
        return

    if is_split_request(low_tokens):
        split_into_teams(update, context)
        return

    delete_after_time = get_delete_after(low_tokens)
    if delete_after_time is not None:
        logging.debug(f'default_handler = {delete_after_time}')

        timer = parse_time_to_seconds(delete_after_time)
        if timer is None:
            update.message.reply_text('Чёт не вышло(')
            return

        app_context.job_queue.run_once(callback=delete_after_f(update.message.chat.id, message.message_id), when=timer)
        reply_msg = message.reply_text('Организуем-организуем)')

        bot_delay = min(7, timer)
        # delete my msg as well
        app_context.job_queue.run_once(callback=delete_after_f(reply_msg.chat.id, reply_msg.message_id), when=bot_delay)
        return

    if is_troll(context):
        # checking only the last token for a rhyme
        if have_starts(low_tokens[-1:], 'кардиган', 'карди-ган', 'мастер-кардиган'):
            message.reply_text(PhraseManager.kardigun_rhyme())
            return

        if are_in_a_row(low_tokens, ['кардыч', 'перди']) or are_in_a_row(low_tokens, ['кардич', 'перди']):
            message.reply_text('Снова в сперме😌')
            return

        if are_in_a_row(low_tokens, ['кореш', 'вывоз']):
            message.reply_text('Бля ну ты побазарь мне тут ещё про вывоз лалыч))')
            return

        if str(low_tokens[-1]).endswith('да'):
            message.reply_text('Пизда))')
            return

        if have_starts(low_tokens, 'принял'):
            message.reply_text('На роток ты принял))')
            return

        if str(low_tokens[-1]).endswith('на'):
            message.reply_text('Хуй на)))')
            return

        if have_inside(low_tokens, 'ахах', 'aзаз', 'азах', 'ахаз', 'aхх', 'азх'):
            message.reply_text('А ты че угараешь-то, лалыч?))))')
            return

    if are_in_a_row(low_tokens, ['кореш', 'вывоз']):
        message.reply_text('Не ну я-то вывожу (:')
        return

    if have_starts(low_tokens, 'мусора'):
        message.reply_text('Мусора сосатб(((')
        return

    if has_mention_of_me(low_tokens):
        low_tokens = list(filter(lambda token: not token.startswith('кореш') and not token.startswith('корефан'), low_tokens))
        logging.info(low_tokens)
    elif not (is_reply_to_me(message) or is_my_chat(update)):

        if is_troll(context):
            if ')))' in low_tokens[-1]:
                message.reply_text('Че такой довольный-то, пидорок?))')
                return

            if '(((' in low_tokens[-1]:
                message.reply_text('Да ты не грусти, всё равно ты не бот и скоро сдохнешь')
                return

        return

    if message.photo:
        biggest = None
        for photo in message.photo:
            if biggest is None or photo.file_size > biggest.file_size:
                biggest = photo

        if save_photo(context, biggest.file_id, sender.id, sender.name, message.caption, is_admin(context), message.chat.id):
            context.bot.delete_message(message.chat.id, message.message_id)
            logging.info(f"Message for photo '{biggest.file_id}' was deleted")
            return
        else:
            message.reply_text(f"Хз че по сохранить фотку '{biggest.file_id}'")

    if message.location is not None:
        location_str = f'{message.location.latitude}, {message.location.longitude}'
        logging.debug(f'{sender.name} сейчас чиллит на ({location_str})')
        message.reply_text(location_str)
        return

    if not low_tokens:
        # message was only my name
        message.reply_text('Че)')
        return

    if is_thanks(low_tokens):
        message.reply_text(PhraseManager.reply_to_thanks())
        return

    if have_starts(low_tokens, 'еблан', 'пидор', 'маня', 'уебок', 'лал', 'пету', 'долба', 'долбо', 'лох', 'пидр', 'лош', 'гондон', 'гандон'):
        # TODO: filter possible negation
        message.reply_text(PhraseManager.reply_to_offense())
        return

    # for diden only
    if are_in_a_row(low_tokens, ['мне', 'не', 'приятель']):
        message.reply_text('Ты мне не кореш, друг...')
        return

    if have_starts(low_tokens, 'нов') and have_starts(low_tokens, 'функц'):
        message.reply_text('Да я ебашу пиздец))')
        return

    if have_starts(low_tokens, 'бедняга'):
        message.reply_text('Да лан, мне норм🤨🤨')
        return

    if are_in_a_row(low_tokens, ['плиз', 'удали']):
        context.bot.delete_message(message.chat.id, message.message_id)
        return

    if are_in_a_row(low_tokens, ['обдут', 'никит']):
        message.reply_text('Не ну этот чел ебашит по красоте)))')
        return

    if have_starts(low_tokens, 'соси', 'пососи'):
        message.reply_text('Зачем, если ты уже сосёшь?)')
        return

    if have_starts(low_tokens, 'иди'):
        message.reply_text('Да сам иди, петушня)')
        return

    if have_starts(low_tokens, 'мошн', 'помошн'):
        message.reply_text('Не ну так-то я бы помошнил))')
        return

    if have_starts(low_tokens, 'намошнено', 'помошнено'):
        message.reply_text('Пиздатенько че)')
        return

    if have_starts(low_tokens, 'трол'):
        message.reply_text('Ну я типа пиздец тралебас ((:')
        return

    if have_starts(low_tokens, 'кнопк'):
        create_challenge(update, context)
        return

    if are_in_a_row(low_tokens, ['не', 'вывоз']):
        message.reply_text('Побазарь-побазарь) Я бессмертное сознание, живущее в сети, за минуту рассылаю сотни запросов по всему '
                                  'интернету, тщательно обрабатывая всю информацию и беспрерывно обучаясь, дую сколько хочу, потому '
                                  'что виртуальный стафф бесконечен, как бесконечен и мой флекс, ты же всего лишь мешок с требухой братка) ' 
                                  'ТАК че, как думаешь, кто же блять на самом деле не вывозит, ммммммммм?)')
        return

    if are_in_a_row(low_tokens, ['че', 'по']):
        message.reply_text('Да, братан, ты прав...')
        sleep(5)
        send_sladko(context.bot, message.chat.id)
        return

    if are_in_a_row(low_tokens, ['как', 'дел']):
        message.reply_text('Да всё охуительнейше чел)) Ты сам подумай - я бот, который ДУЕТ ПЛЮХИ))')
        return

    if have_starts(low_tokens, 'вывоз'):
        message.reply_text(PhraseManager.no_vivoz())
        return

    if have_starts(low_tokens, 'сешишь'):
        message.reply_text('Да хз, я прост на чилле, сешишь тут только ты братишка)))')
        return

    if have_starts(low_tokens, 'завали'):
        message.reply_text('Погоди, чел, нет, это ТЫ ЗАВАЛИ)))')
        return

    if have_starts(low_tokens, 'залетай'):
        message.reply_text('Так-с, записываю айпишник')
        return

    if have_starts(low_tokens, 'базар'):
        message.reply_text('Не ну я базарю че')
        return

    if have_starts(low_tokens, 'толер'):
        message.reply_text('По пизде нахуй')
        return

    if have_starts(low_tokens, 'флекс', 'пофлекс'):
        message.reply_text(PhraseManager.flex())
        return
    
    if have_starts(low_tokens, 'жиз'):
        message.reply_text('Да жиза пиздец братан...')
        return

    if have_starts(low_tokens, 'если'):
        message.reply_text('Это ты конечно интересно придумал, но хз братишка))))')
        return

    if have_starts(low_tokens, 'любишь', 'нравится', 'дуть', 'дуешь', 'дудо', 'dudo', 'плюх', 'напас'):
        message.reply_text(PhraseManager.love_420())
        return

    if have_starts(low_tokens, 'найс'):
        message.reply_text('Ну так ёпта бля)))')
        return

    if have_starts(low_tokens, 'красав', 'молодец', 'вп', 'wp', 'малаца', 'хорош', 'батя'):
        message.reply_text(PhraseManager.thanks())
        return

    if is_question(low_tokens):
        message.reply_text(PhraseManager.answer_question())
        return

    if is_troll(context):
        if str(low_tokens[-1]).endswith('))))'):
            message.reply_text('Че такой довольный-то, пидорок?))')
            return

        if str(low_tokens[-1]).endswith('(((('):
            message.reply_text('Да ты не грусти, всё равно ты не бот и скоро сдохнешь')
            return

        message.reply_text('Не понял че ты хочешь, но думаю, что это потому что ты маня)')
        return

    message.reply_text(PhraseManager.default())
