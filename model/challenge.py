from dataclasses import dataclass, field
from datetime import timedelta, datetime
from functools import cached_property
from typing import Dict, Set

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, ParseMode

from model.emojis import Emojis
from utils.str_utils import timedelta_to_str, tries_to_str


@dataclass
class Winner:
    name: str
    duration: timedelta
    push_cnt: int = 1

    def to_str(self) -> str:
        res = f'{self.name} [{round(self.duration.total_seconds(), 1)}s]'
        if self.push_cnt > 1:
            comment_str = 'люто'
            if self.push_cnt >= 10:
                comment_str = 'но нахуя?'
            if self.push_cnt >= 50:
                comment_str = 'минус кукуха'
            res += f' (аж {tries_to_str(self.push_cnt)} нажал, {comment_str})'
        return res


@dataclass
class Challenge:
    id: int
    chat_id: int
    msg_id: int
    author: str
    duration: timedelta
    started_at: datetime
    text: str
    winners: Dict[str, Winner] = field(default_factory=dict)
    traitors: Set[str] = field(default_factory=set)

    @cached_property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton(f'{Emojis.GREEN_CHECK_MARK} ЖМЯК', callback_data=f'+ {self.id}'),
             InlineKeyboardButton(f'{Emojis.RED_CROSS} Минус', callback_data=f'- {self.id}')]]
        )

    def is_finished(self) -> bool:
        return datetime.now() - self.started_at > self.duration

    def post_update(self, bot: Bot):
        reply_markup = self.reply_markup if not self.is_finished() else None
        bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.msg_id,
            text=self.get_text_for_current_state(datetime.now()),
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    def get_text_for_current_state(self, now: datetime):
        just_list_str = '\n'.join([f'{i}. {w.to_str()}' for i, w in enumerate(self.winners.values(), 1)]) + '\n\n'
        winners_str = f'Залетели по красоте:\n{just_list_str}' if not len(self.winners) == 0 else ''
        traitors_str = 'Аутотренят по полной:\n' + '\n'.join(self.traitors) + '\n\n' if not len(self.traitors) == 0 else ''

        '\n'.join([f'{i}. {w.to_str()}' for i, w in enumerate(self.winners.values(), 1)]) + '\n\n'

        spent = now - self.started_at
        remains_str = f'<i>Осталось {timedelta_to_str(self.duration - spent)}!</i>' if spent < self.duration else ''

        res = f'{self.text}\n\n' \
              f'{winners_str}'  \
              f'{traitors_str}' \
              f'{remains_str}'

        return res
