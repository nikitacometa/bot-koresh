from time import sleep

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action


def is_troll(context: CallbackContext) -> bool:
    if context.chat_data.get('troll_mode') is None:
        context.chat_data['troll_mode'] = True
    return context.chat_data['troll_mode']


@send_action(ChatAction.TYPING)
@moshnar_command
def troll_mode(update: Update, context: CallbackContext):
    if not context.args:
        if is_troll(context):
            update.message.reply_text('Ну и что лол? Челик ты вообще тут??)')
        else:
            update.message.reply_text('Нужно ещё передать on/off)')
        return

    token = str(context.args[0]).lower()
    if token == 'off':
        troll_mode_off(update, context)
    elif token == 'on':
        troll_mode_on(update, context)
    else:
        if is_troll(context):
            update.message.reply_text('on/off, `ёбобо))')
        else:
            update.message.reply_text('Нужно ещё передать on/off')


def troll_mode_on(update: Update, context: CallbackContext):
    if context.chat_data.get('troll_mode', False):
        update.message.reply_text('Не увидел мой троллинг? Потому что он в твоей жопе')
        return

    context.chat_data['troll_mode'] = True
    update.message.reply_text('Время подор-вать')
    sleep(3)
    update.message.reply_text('Петушкам пердачки)))')


def troll_mode_off(update: Update, context: CallbackContext):
    if not context.chat_data.get('troll_mode', True):
        update.message.reply_text('Да я и так никого не троллю...')
        return

    update.message.reply_text('Лан-лан...')
    context.chat_data['troll_mode'] = False
