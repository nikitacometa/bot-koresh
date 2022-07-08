from dataclasses import dataclass
from typing import Callable, Optional

from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext


class HelpLine:
    def text(self) -> str:
        pass


@dataclass
class Separator(HelpLine):
    text: str


@dataclass
class Command(HelpLine):
    name: str
    handler: Callable[[Update, CallbackContext], None] = None
    help: Optional[str] = None

    additional_dispatcher_update: Optional[Callable] = None

    def update_dispatcher(self, dp: Dispatcher) -> None:
        dp.add_handler(CommandHandler(self.name, self.handler))
        if self.additional_dispatcher_update:
            self.additional_dispatcher_update(dp)

    @property
    def text(self) -> str:
        return self.help
