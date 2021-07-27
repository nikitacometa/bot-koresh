from datetime import timedelta
from typing import Optional

from telegram.ext import CallbackContext


def vanish_after(context: CallbackContext) -> Optional[timedelta]:
    return context.chat_data.get('vanish_mode')


def is_vanishing(context: CallbackContext) -> bool:
    return vanish_after(context) is not None
