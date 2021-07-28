import os
import random

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action
from app.utils.message_utils import send_message


def get_anek() -> str:
    files = os.listdir('aneks')
    aneks = list(filter(lambda x: x.startswith('anek'), files))
    print(f'Total {len(aneks)} aneks')
    anek_name = f'aneks/{random.choice(aneks)}'
    f = open(anek_name, 'r')
    return fix_emojis(f.read())


@moshnar_command
@send_action(ChatAction.TYPING)
def joke(update: Update, context: CallbackContext):
    story = f'{get_anek()}'
    send_message(context, update, story)


def fix_emojis(s: str) -> str:
    while True:
        pattern = '<img alt="'
        begin = s.find(pattern)
        if begin == -1:
            break

        next = begin + len(pattern)
        emoji = s[next]

        pattern = 'png"/>'
        png = s.find(pattern)
        end = png + len(pattern)
        s = s[:begin] + emoji + s[end:]

    return s
