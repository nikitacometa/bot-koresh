import logging

from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from managers.phrase_manager import PhraseManager
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action


@send_action(ChatAction.TYPING)
@moshnar_command
def start(update: Update, context: CallbackContext):
    try:
        update.message.reply_text(PhraseManager.greet())
    except Exception as ex:
        logging.exception(ex)
