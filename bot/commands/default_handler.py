import logging
from datetime import datetime, timedelta
from time import sleep
from typing import List

from telegram import Update, Message, User
from telegram.ext import CallbackContext

from bot.commands.admin_mode import try_process_admin_command
from bot.commands.joke import get_anek
from bot.commands.create_challenge import create_challenge
from bot.commands.show_map import extract_coordinates
from bot.commands.track_address import track_address
from bot.commands.troll_mode import is_troll
from bot.commands.delete_after import get_delete_after
from bot.commands.save_photo import save_photo
from bot.commands.split_teams import split_into_teams, is_splitting
from bot.commands.vanish_mode import is_vanishing
from bot.context import app_context, settings
from bot.validator import is_valid_bitcoin_address
from managers.phrase_manager import PhraseManager
from utils.classes.moshnar_command import moshnar_command
from utils.message_utils import send_sladko, delete_msg_after, send_message, vanish

# TODO: make parse_utils or Parser
from utils.parse_utils import get_alpha_part
from utils.str_utils import parse_time_to_seconds


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
    return update.message.chat.id == settings.bot_chat_id


def is_split_request(tokens: List[str]) -> bool:
    return have_start_in_list(tokens, ['подели', 'намошни', 'раздели', 'посплить']) and \
           have_start_in_list(tokens, ['плиз', 'плз', 'плез', 'пож', 'по-братски'])


def is_question(tokens: List[str]) -> bool:
    return '?' in tokens[-1]


def is_sladko(msg: Message) -> bool:
    if msg.sticker is None:
        return False

    return msg.sticker.file_unique_id == 'AgADBgADhlyiAw'


def handle_sladko(msg: Message, context: CallbackContext) -> bool:
    context.chat_data['sladko_prev'] = context.chat_data.get('sladko_cur')
    context.chat_data['sladko_cur'] = is_sladko(msg)

    if context.chat_data.get('sladko_cur') and context.chat_data.get('sladko_prev'):
        context.chat_data['sladko_cur'] = False
        send_sladko(context.bot, msg.chat.id)

    return is_sladko(msg)


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

    if handle_sladko(message, context):
        return

    if is_splitting(text):
        context.chat_data['not_a_command'] = True
        split_into_teams(update, context)
        return

    if sender.username == 'Luckmannn':
        # TODO: store this info in DB
        # TODO: set this feature via command
        now = datetime.now()
        if now - app_context.last_hi_mark_at > settings.hi_mark_delay_h * 24:
            send_message(context, update, 'ooh hi Mark)')
            app_context.last_hi_mark_at = now

    try:
        coords = extract_coordinates(tokens)
        if coords:
            img_link = app_context.map_client.get_img_link_by_coordinates(coords)
            reply = update.message.reply_photo(photo=img_link)
            vanish(reply, context)
    except Exception as e:
        logging.exception(e)

    # TODO: reformat for easy creating of new situations/cases
    for s in tokens:
        try:
            alpha_part = get_alpha_part(s)
            if is_valid_bitcoin_address(alpha_part):
                try:
                    track_address(alpha_part, message, context.bot)
                except Exception as e:
                    logging.exception(e)
            return
        except Exception:
            pass

    delete_after_time = get_delete_after(low_tokens)
    if delete_after_time is not None:
        logging.debug(f'default_handler = {delete_after_time}')

        timer = parse_time_to_seconds(delete_after_time)
        if timer is None:
            send_message(context, update, 'Чёт не вышло(')
            return

        delete_msg_after(update.message.chat.id, message.message_id, timedelta(seconds=timer))
        reply_msg = send_message(context, update, 'Организуем-организуем)')

        bot_delay = min(7, timer)
        # delete my msg as well
        delete_msg_after(reply_msg.chat.id, reply_msg.message_id, timedelta(seconds=bot_delay))
        return

    if is_vanishing(context):
        return

    # TODO: make an option
    saving_photos = False
    if saving_photos and message.photo:
        biggest = None
        for photo in message.photo:
            if biggest is None or photo.file_size > biggest.file_size:
                biggest = photo

        if save_photo(context, biggest.file_id, sender.id, sender.name, message.caption, message.chat.id):
            context.bot.delete_message(message.chat.id, message.message_id)
            logging.info(f"Message for photo '{biggest.file_id}' was deleted")
            return
        else:
            send_message(context, update, f"Хз че по сохранить фотку '{biggest.file_id}'")

    if message.location is not None:
        location_str = f'{message.location.latitude}, {message.location.longitude}'
        logging.debug(f'{sender.name} сейчас чиллит на ({location_str})')
        send_message(context, update, location_str)
        return

    if text is None:
        return
    # after that just text handlers

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

        if have_starts(low_tokens, 'алиса'):
            message.reply_text('Хуиса ёпт. Ты дебил?')
            return

        if have_starts(low_tokens, 'метнись'):
            message.reply_text('А ты давай-ка на парашу метнись)')
            return

        if str(low_tokens[-1]).endswith('на'):
            message.reply_text('Хуй на)))')
            return

        if str(low_tokens[-1]) == 'мило':
            message.reply_text('Ну а ты хуила)')
            return

        if have_inside(low_tokens, 'ахах', 'aзаз', 'азах', 'ахаз', 'aхх', 'азх'):
            message.reply_text(PhraseManager.laugh_reaction())
            return

    if are_in_a_row(low_tokens, ['кореш', 'вывоз']):
        message.reply_text('Не ну я-то вывожу (:')
        return

    if have_starts(low_tokens, 'мусора') or have_starts(low_tokens, 'мент'):
        message.reply_text('Мусора сосать))')
        return

    if are_in_a_row(low_tokens, ['иди', 'на']):
        message.reply_text('Там уже занято тобой :(')
        return

    try:
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
    except Exception as e:
        logging.exception(e)

    if have_starts(low_tokens, 'анек', 'истори', 'расскаж') and have_start_in_list(low_tokens, PhraseManager.PLEASE_WORDS):
        send_message(context, update, get_anek())
        return

    if have_starts(low_tokens, 'прив', 'даров', 'йо', 'алоха', 'вазап'):
        send_message(context, update, PhraseManager.greet())
        return

    if not low_tokens:
        # message was only my name
        message.reply_text('Че)')
        return

    if low_tokens[0].startswith('поясн') or low_tokens[0].startswith('скаж'):
        message.reply_text(PhraseManager.telling_response())
        return

    if len(low_tokens) == 1 and low_tokens[0].startswith('чел'):
        message.reply_text(PhraseManager.chel_response())
        return

    if len(low_tokens) == 1 and have_starts(low_tokens, 'брат', 'друг', 'приятель', 'друж'):
        send_message(context, update, PhraseManager.nice_call_response())
        return

    if is_thanks(low_tokens):
        message.reply_text(PhraseManager.reply_to_thanks())
        return

    if have_starts(low_tokens, 'еблан', 'пидор', 'маня', 'уебок', 'лал', 'пету', 'долба', 'долбо', 'лох', 'пидр', 'лош', 'гондон', 'гандон'):
        # TODO: filter possible negation
        message.reply_text(PhraseManager.reply_to_offense())
        return

    if are_in_a_row(low_tokens, ['зачитай', 'реп']) or are_in_a_row(low_tokens, ['зачитай', 'рэп']):
        message.reply_text('Я пиздатый бот, ебал вас всех в рот\nМой создатель бог, ты же просто лох\nЯ ебашу в кашу, ты сидишь на параше\nХочешь быть как я? Иди на хуй')
        return

    if are_in_a_row(low_tokens, ['прочитай', 'реп']) or are_in_a_row(low_tokens, ['прочитай', 'рэп']):
        message.reply_text('Я пиздатый бот, ебал вас всех в рот\nМой создатель бог, ты же просто лох\nЯ ебашу в кашу, ты сидишь на параше\nХочешь быть как я? Иди на хуй')
        return

    if have_starts(low_tokens, 'создатель'):
        message.reply_text('Мой создатель бог, ты же просто лох')
        return

    # for diden only
    if are_in_a_row(low_tokens, ['мне', 'не', 'приятель']):
        message.reply_text('Ты мне не кореш, друг...')
        return

    if are_in_a_row(low_tokens, ['мне', 'не', 'кореш']):
        message.reply_text('Ну и иди нахуй тогда че)')
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

        message.reply_text(PhraseManager.no_understand())
        return

    message.reply_text(PhraseManager.default())
