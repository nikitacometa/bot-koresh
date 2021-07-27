from datetime import timedelta

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from app.managers.phrase_manager import PhraseManager
from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action
from app.utils.message_utils import delete_after
from app.utils.modes import is_vanishing, vanish_after
from app.utils.str_utils import parse_time, timedelta_to_str

DEFAULT_VANISH_DELAY = timedelta(hours=1)
DELETE_DELAY = timedelta(seconds=6)
TIME_TAGS_EXAMPLE = "$10s, $20m, $2h, $1d, $..."

@send_action(ChatAction.TYPING)
@moshnar_command
def vanish_mode(update: Update, context: CallbackContext):
    if not context.args:
        if is_vanishing(context):
            delete_after(update.message, DELETE_DELAY)
            rep = update.message.reply_text(f'Я и так удаляю все сообщения через {vanish_after(context)}')
            delete_after(rep, DELETE_DELAY)
            return
        remove_after = DEFAULT_VANISH_DELAY
    else:
        token = str(context.args[0]).lower()
        if token == 'off':
            vanish_mode_off(update, context)
            return
        elif token == 'on':
            remove_after = DEFAULT_VANISH_DELAY
        else:
            remove_after = parse_time(token)

    if remove_after is None:
        update.message.reply_text(f'Надо бы время ещё передать, приятель ({TIME_TAGS_EXAMPLE})')
        return

    context.chat_data['vanish_mode'] = remove_after
    rep = update.message.reply_text(f'{PhraseManager.no_problem()}\nБуду удалять сообщения через {timedelta_to_str(remove_after)}')

    delete_after(update.message, DELETE_DELAY)
    delete_after(rep, DELETE_DELAY)


def vanish_mode_off(update: Update, context: CallbackContext):
    if not is_vanishing(context):
        update.message.reply_text('Да я и так ничего не удалял')
        return

    update.message.reply_text(f'{PhraseManager.ok()}, не буду удалять')
    context.chat_data['vanish_mode'] = None
