import logging
from datetime import timedelta
from typing import Optional

from telegram import Bot, ParseMode, Message, Update
from telegram.ext import CallbackContext

from model.stickers import Stickers
from utils.modes import is_vanishing, vanish_after
from utils.str_utils import tx_info_to_str, get_addr_html_url, datetime_to_str
from model.tracking import Tracking


def send_message(context: CallbackContext, update: Update, text: str) -> Message:
    return send_message_to_chat(context, update.message.chat.id, text)

# TODO: refactor these two /\ \/


def send_message_to_chat(context: CallbackContext, chat_id: int, text: str) -> Message:
    reply = context.bot.send_message(chat_id, text)
    if is_vanishing(context):
        delete_after(reply, vanish_after(context))
    return reply


def send_tx_info(t: Tracking, msg: Optional[str] = None):
    return send_tracking_info_full(t, msg_after=msg)


def send_tracking_info_full(t: Tracking, msg_before: Optional[str] = None, msg_after: Optional[str] = None):
    txs_str = '\n\n'.join([tx_info_to_str(tx_info) for tx_info in t.transactions])
    upd_str = f'<code>[updated {datetime_to_str(t.updated_at)}]</code>'
    output = f'<code>[</code>{get_addr_html_url(t.address)}<code>]</code>\n{txs_str}\n{upd_str}\n'
    if msg_before is not None:
        output = f'{msg_before}\n\n' + output
    if msg_after is not None:
        output += f'\n{msg_after}'

    return comment_tracking(t, output)


def comment_tracking(t: Tracking, msg: str):
    logging.debug(f'Commenting... {t.address}')

    # TODO: fix local
    from bot.context import app_context
    return app_context.bot.send_message(text=msg, chat_id=t.chat_id, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


def send_sladko(bot: Bot, chat_id):
    bot.send_sticker(chat_id, Stickers.SLADKO)


def delete_after_f(chat_id: int, message_id: int):
    def delete_after(context: CallbackContext):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    return delete_after


def delete_msg_after(chat_id: int, msg_id: int, t: timedelta):
    from bot.context import app_context
    app_context.job_queue.run_once(callback=delete_after_f(chat_id, msg_id), when=t)


def delete_after(msg: Message, t: timedelta):
    delete_msg_after(msg.chat_id, msg.message_id, t)


def vanish(msg: Message, context: CallbackContext):
    if is_vanishing(context):
        delete_after(msg, vanish_after(context))


def send_sesh(bot: Bot, chat_id):
    bot.send_sticker(chat_id, Stickers.SESH)
