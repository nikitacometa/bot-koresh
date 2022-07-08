from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from bot.commands.commands import Commands
from managers.phrase_manager import PhraseManager
from utils.classes.moshnar_command import moshnar_command
from utils.classes.sending_action import send_action


@send_action(ChatAction.TYPING)
@moshnar_command
def show_help(update: Update, context: CallbackContext):
    msg = f'{PhraseManager.how_are_you(update.message.from_user.first_name)}\n'
    msg += '\n'
    msg += 'Поздравляю, наконец в твоей жизни появился смысл!'
    msg += 'Теперь ты можешь бесцельно развлекать себя и своих кожаных собратьев разными странными способами:\n'
    msg += '\n'
    msg += Commands.help_string()

    update.message.reply_text(msg)
