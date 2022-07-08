from typing import Any

from telegram.ext import CallbackContext


def increase_messages_count(context: CallbackContext):
    context.chat_data['msg_cnt'] = context.chat_data.get('msg_cnt', 0) + 1
    return context.chat_data['msg_cnt']


def set_chat_data(context: CallbackContext, name: str, value: Any):
    context.chat_data[name] = value


def get_chat_data(context: CallbackContext, name: str, default_value: Any = None):
    if name not in context.chat_data and default_value is not None:
        context.chat_data[name] = default_value
    return context.chat_data[name]
