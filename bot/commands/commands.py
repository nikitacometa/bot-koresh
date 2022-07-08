from dataclasses import dataclass
from typing import ClassVar, List

from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from bot.commands.joke import joke
from bot.commands.show_map import show_map
from bot.commands.abstract_command import Command, HelpLine, Separator
from bot.commands.admin_mode import admin_mode
from bot.commands.create_challenge import handle_challenge, challenge_update_dispatcher
from bot.commands.translate import translate_handle
from bot.commands.vanish_mode import vanish_mode, TIME_TAGS_EXAMPLE
from bot.commands.show_tracked import show_tracked
from bot.commands.split_teams import split_into_teams
from bot.commands.start import start
from bot.commands.track_address import track_address_handler
from bot.commands.troll_mode import troll_mode
from managers.phrase_manager import PhraseManager
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action


@send_action(ChatAction.TYPING)
@moshnar_command
def show_help(update: Update, context: CallbackContext):
    msg = f'{PhraseManager.how_are_you(update.message.from_user.first_name)}\n'
    msg += '\n'
    msg += 'Поздравляю, наконец в твоей жизни появился смысл!'
    msg += 'Теперь ты можешь бесцельно развлекать себя и своих кожаных собратьев разными странными способами:\n'
    msg += '\n'
    msg += Commands.help_string()
    msg += '\n\n'
    msg += 'Кстати, я люблю поболтать. Добавляй в конфы - наводи шуму. '
    msg += 'Но прошу не обижаться на мои базары, я просто делаю свою работу.'

    update.message.reply_html(msg, disable_web_page_preview=True)


@dataclass
class Commands:
    help_lines: ClassVar[List[HelpLine]] = [
        Command('start', start),


        Separator('<b>Bitcoin движ</b>'),

        # TODO: change to check + button for tracking
        Command('track', track_address_handler, help=
                f'/track <b>$addr</b> – понаблюдаю за адресом и сразу отпишу, как только на последней/новой транзакции '
                f'наберётся нужное количество подтверждений (по дефолту 2)'),

        Command('show_tracked', show_tracked, help=
                f'/show_tracked – показать все отслеживаемые адреса'),


        Separator('\n<b>Для тех, у кого есть друзья</b>'),

        Command('split_teams', split_into_teams, help=
                f'/split_teams – поделить список людей на n команд (2 по дефолту), каждое имя на отдельной строке'),

        Command('challenge', handle_challenge, additional_dispatcher_update=challenge_update_dispatcher, help=
                f'/challenge <b>$t</b> – скинуть в чат кнопку "кто быстрее нажмёт" на $t ({TIME_TAGS_EXAMPLE}) времени, '
                f'если вдруг надо набрать поскорее сколько-то людей (опционально добавляем текст)'),


        Separator('\n<b>Для тебя (ведь ты любишь путешествия и поржать)</b>'),

        # TODO: don't write name in help (add it in Command init)
        Command('show_map', show_map,
                help=f'/show_map <b>$x, $y</b> – показать кусок карты по данным координатам'),

        Command('joke', joke, help=f'/joke – расскажу один из анеков своего деда'),


        Separator('\n<b>Chat settings</b>'),

        Command('troll_mode', troll_mode,
                help=f'/troll_mode <b>on/off</b> – я конечно не GPT, но матом покрою от души'),

        Command('vanish_mode', vanish_mode,
                help=f'/vanish_mode <b>$t/off</b> – удалять все сообщения в чате через t ({TIME_TAGS_EXAMPLE})'),

        # something

        Command('admin_mode', admin_mode),

        Command('translate', translate_handle),

        Command('help', show_help)
    ]

    @classmethod
    def help_string(cls) -> str:
        return '\n'.join(list(filter(None, map(lambda line: line.text, cls.help_lines))))

    @classmethod
    def get_all(cls) -> List[Command]:
        return [l for l in cls.help_lines if isinstance(l, Command)]
