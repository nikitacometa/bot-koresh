import logging

from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from model.tracking import AddressStatus
from bot.context import app_context
from managers.phrase_manager import PhraseManager
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action
from utils.message_utils import send_tx_info


@send_action(ChatAction.TYPING)
@moshnar_command
def show_tracked(update: Update, context: CallbackContext):
    try:
        if context.args and context.args[0] == 'fucking_all':
            tracked = app_context.tracking_manager.get_all()
        else:
            tracked = app_context.tracking_manager.get_by_chat_id(update.message.chat.id)

        if not tracked:
            update.message.reply_html(PhraseManager.nothing_to_do())
            return

        for t in tracked:
            updated = app_context.tracking_manager.update_tracking(t)
            send_tx_info(updated)
            if updated.status == AddressStatus.CONFIRMED:
                if app_context.tracking_manager.remove_tracking(updated):
                    logging.debug(f'Address {updated.address} was removed.')
                else:
                    logging.debug(f'Failed to remove address {updated.address}.')

    except Exception as e:
        logging.exception(e)
