import atexit
import logging

from telegram.ext import MessageHandler, Filters

from bot.commands.abstract_command import Command
from bot.commands.commands import Commands
from bot.commands.default_handler import default_message_handler
from bot.context import app_context

# TODO: make him inline to have an ability to use it in every conversation
# TODO: separate class
from bot.updater import run_info_updater_if_not


def run():
    updater = app_context.updater
    dp = updater.dispatcher

    for command in Commands.get_all():
        if isinstance(command, Command):
            command.update_dispatcher(dp)

    # fallback
    dp.add_handler(MessageHandler(Filters.all, default_message_handler))

    updater.start_polling()

    run_info_updater_if_not()

    logging.info('Bot started!\n\nWell... Hello (:\n')

    # TODO: to settings
    # fetch_aneks()

    updater.idle()


def tear_down():
    logging.info('EXIT BOT\n\nBye!\n')


if __name__ == '__main__':
    atexit.register(tear_down)

    try:
        run()
    except Exception as ex:
        logging.exception(ex)
