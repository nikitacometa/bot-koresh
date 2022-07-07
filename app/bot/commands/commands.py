from dataclasses import dataclass
from typing import ClassVar, List

from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from app.bot.commands.joke import joke
from app.bot.commands.show_map import show_map
from app.bot.commands.abstract_command import Command
from app.bot.commands.admin_mode import admin_mode
from app.bot.commands.create_challenge import handle_challenge, challenge_update_dispatcher
from app.bot.commands.translate import translate_handle
from app.bot.commands.vanish_mode import vanish_mode, TIME_TAGS_EXAMPLE
from app.bot.commands.show_tracked import show_tracked
from app.bot.commands.split_teams import split_into_teams
from app.bot.commands.start import start
from app.bot.commands.track_address import track_address_handler
from app.bot.commands.troll_mode import troll_mode

from app.managers.phrase_manager import PhraseManager
from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action


@send_action(ChatAction.TYPING)
@moshnar_command
def show_help(update: Update, context: CallbackContext):
    msg = f'{PhraseManager.how_are_you()}, {update.message.from_user.first_name})\n'
    msg += '\n'
    msg += 'Вообще я так-то 10/10 бот и выкупаю все команды и без ключевых слов, но на случай если ты вдруг не особо '
    msg += 'просекаешь базары или просто не вывозишь, вот тебе список доступных ключевых команд:\n'
    msg += '\n'
    msg += '\n'.join(list(filter(None, map(lambda cmd: cmd.help, Commands.get_all()))))
    update.message.reply_text(msg)


# TODO: naming
@dataclass
class Commands:
    _all: ClassVar[List[Command]] = [
        Command('start', start),

        # TODO: change to check + button for tracking
        Command('track', track_address_handler, help=
                f'/track - попалить, '
                f'какая последняя транзакция на адресе(-ах), и если она есть и ещё не '
                f'дошла, то пиздец пристально последить за ней и СРАЗУ ЖЕ отписать в чат, когда она дойдёт)'),

        Command('show_tracked', show_tracked, help=
                f'/show_tracked - показать все отслеживаемые адреса\n'),

        Command('split_teams', split_into_teams, help=
                f'/split_teams - поделить множество людей на n команд (2 по дефолту)'),

        # TODO: don't write name in help (add it in Command init)
        Command('show_map', show_map, help=
                f'/show_map - показать кусок карты по данной локации'),

        Command('admin_mode', admin_mode),

        Command('translate', translate_handle),

        Command('challenge', handle_challenge, additional_dispatcher_update=challenge_update_dispatcher, help=
                f'/challenge $t - скинуть в чат кнопку "кто быстрее" на t ({TIME_TAGS_EXAMPLE}) времени, если вдруг надо что-то серьёзное быстро порешать'),

        Command('joke', joke, help=f'/joke - расскажу анек чисто)\n'),

        Command('troll_mode', troll_mode, help=
                f'/troll_mode on/off - тролльмод'),

        Command('vanish_mode', vanish_mode,
                help=f'/vanish_mode $t/off - удалять все сообщения в чате через t ({TIME_TAGS_EXAMPLE})'),

        Command('help', show_help)
    ]

    @classmethod
    def get_all(cls) -> List[Command]:
        return cls._all
