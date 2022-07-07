from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from app.managers.anek_manager import get_anek
from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action
from app.utils.message_utils import send_message


@moshnar_command
@send_action(ChatAction.TYPING)
def joke(update: Update, context: CallbackContext):
    send_message(context, update, get_anek())
