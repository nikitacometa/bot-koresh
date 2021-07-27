from telegram import Update, ChatAction, Message, User
from telegram.ext import CallbackContext

from app.bot.context import app_context
from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action


@send_action(ChatAction.TYPING)
@moshnar_command
def translate_handle(update: Update, context: CallbackContext) -> None:
    message: Message = update.message
    sender: User = message.from_user
    text: str = message.text
    tokens = text.split() if text is not None else []
    if not tokens:
        # can't be ever
        return

    command_len = len(tokens[0])
    text = text[command_len:]

    translated = app_context.translator_client.translate(text)
    update.message.reply_text(translated)
