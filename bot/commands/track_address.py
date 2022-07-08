import logging
from typing import Optional

from telegram import ChatAction, Update, Message, Bot, ParseMode
from telegram.ext import CallbackContext

from env import TRACKING_TTL
from model.tracking import Tracking, AddressStatus
from bot.context import app_context
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action
from utils.message_utils import send_tracking_info_full, send_tx_info, send_message_to_chat, send_message
from utils.str_utils import get_addr_html_url, timedelta_to_str


def track_address(address: str, message: Message, bot: Bot) -> Optional[Tracking]:
    found = app_context.tracking_manager.get_tracking_by_address(address)
    if found is not None:
        # TODO: handle tx finished
        send_tracking_info_full(found, 'Чел, да я и так палю че по...')
        return found

    try:
        status, tx_info = app_context.blockchain_client.check_address(address)
    except Exception as e:
        logging.exception(e)
        return None

    if status == AddressStatus.INVALID_HASH:
        message.reply_text(f'Это хуйня, а не адрес, чел)) {address} - че?)')
        return None

    if status == AddressStatus.CHECK_FAILED:
        message.reply_text(f'Хз че по {address}, сеш (какой-то).')
        return None

    if status == AddressStatus.CONFIRMED:
        # TODO: send how long ago
        message.reply_text('УЖЕ намошнено ЧЕЛ))')
        return None

    chat_id = message.chat.id
    new_tracking = app_context.tracking_manager.create(address, chat_id, status, [tx_info])
    if status == AddressStatus.NO_TRANSACTIONS:
        bot.send_message(chat_id, f'Эх, пока ни одной транзакции на {get_addr_html_url(address)}...\n'
                                  f'Но я понаблюдаю за ним {timedelta_to_str(TRACKING_TTL)}, отпишу ес че',
                         parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    if status == AddressStatus.NOT_CONFIRMED:
        if tx_info.conf_cnt == 0:
            send_tx_info(new_tracking, 'Так-с, на адреске чёт пока нихуя, но я попалю хули) Базар-вокзал))')
        else:
            send_tx_info(new_tracking, 'Не ну))) Уже прям найс) Я попалю когда там че будет прям збс типа окда)')

    return new_tracking


@send_action(ChatAction.TYPING)
@moshnar_command
def track_address_handler(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if not args:
            send_message(context, update, f'Анус себе потрекай братишка))')
            return

        for address in args:
            if address == 'random':
                address = app_context.blockchain_client.get_random_address_with_unconfirmed_tx()

            track_address(address, update.message, context.bot)

    except Exception as e:
        logging.exception(e)
