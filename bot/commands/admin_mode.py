import logging

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action


def is_admin(context: CallbackContext) -> bool:
    return context.chat_data.get('admin_mode', False)


@send_action(ChatAction.TYPING)
@moshnar_command
def admin_mode(update: Update, context: CallbackContext) -> None:
    if not context.args:
        if context.chat_data.get('troll_mode', False):
            update.message.reply_text('Бля ну и че) Ты вообще вывозишь?)')
        else:
            update.message.reply_text('Нужно ещё передать on/off)')
        return

    token = str(context.args[0]).lower()
    if token == 'off':
        admin_mode_off(update, context)
    elif token == 'on':
        admin_mode_on(update, context)
    else:
        if context.chat_data.get('troll_mode', False):
            update.message.reply_text('on/off, `ёбобо))')
        else:
            update.message.reply_text('Нужно ещё передать on/off')


def admin_mode_on(update: Update, context: CallbackContext) -> None:
    if context.chat_data.get('admin_mode', False):
        update.message.reply_text('Да уже.')
        return

    context.chat_data['admin_mode'] = True
    update.message.reply_text('Отлично, работаем дальше!')


def admin_mode_off(update: Update, context: CallbackContext) -> None:
    if not context.chat_data.get('admin_mode', True):
        update.message.reply_text('И так нет.')
        return

    update.message.reply_text('Эх, жаль.')
    context.chat_data['admin_mode'] = False


def try_process_admin_command(update: Update, context: CallbackContext) -> bool:
    if not is_admin(context):
        return False

    logging.debug(f'admin command')

    return False
