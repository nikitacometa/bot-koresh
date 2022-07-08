from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from managers.anek_manager import get_anek
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action
from utils.message_utils import send_message


@moshnar_command
@send_action(ChatAction.TYPING)
def joke(update: Update, context: CallbackContext):
    send_message(context, update, get_anek())
