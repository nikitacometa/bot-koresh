from typing import List, Optional

from telegram.ext import CallbackContext


def get_delete_after(tokens: List[str]) -> Optional[str]:
    option = list(filter(lambda token: token.startswith('$') and token[-1] in 'smhd', tokens))
    return option[0] if len(option) > 0 else None


def delete_after_f(chat_id: int, message_id: int):
    def delete_after(context: CallbackContext):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    return delete_after
