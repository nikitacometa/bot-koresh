import logging
import time
from functools import wraps

from telegram import Update, User, Message
from telegram.ext import CallbackContext

from bot.context import app_context
from env import SLADKO_EVERY_N, COMMAND_RETRIES, SAVE_LAST_MESSAGES_CNT
from utils.message_utils import send_sladko, delete_after
from utils.callback_context_utils import increase_messages_count


def moshnar_command(command_handler):
    @wraps(command_handler)
    def wrapper(*args, **kwargs):
        update: Update = args[0]
        context: CallbackContext = args[1]
        message: Message = update.message

        logging.debug(f"Processing new input: '{message.text}'")

        if 'id' not in context.chat_data:
            try:
                context.chat_data['id'] = message.chat.id
            except Exception:
                pass

        if 'last_msgs' not in context.chat_data:
            context.chat_data['last_msgs'] = []

        last_msgs = context.chat_data.get('last_msgs')
        if len(last_msgs) >= SAVE_LAST_MESSAGES_CNT:
            last_msgs.pop(0)
        last_msgs.append(message)

        vanish_after = context.chat_data.get('vanish_mode')
        if vanish_after is not None:
            delete_after(message, vanish_after)

        for i in range(COMMAND_RETRIES + 1):
            try:
                start_time = time.time()

                res = command_handler(update, context)
                msg_cnt = increase_messages_count(context)
                if msg_cnt % SLADKO_EVERY_N == 0:
                    send_sladko(app_context.bot, message.chat.id)

                execution_time = time.time() - start_time
                # TODO: log uptime
                logging.debug(f'Done in {round(execution_time, 3)}s, msg_cnt since restart = {msg_cnt}')

                user: User = message.from_user
                user_info = app_context.db_manager.users.find_one({'id': user.id})

                if user_info is None:
                    init_info = {
                        'id': user.id,
                        'name': user.name,
                        'msg_cnt': 1
                    }
                    res = app_context.db_manager.users.insert_one(init_info)
                    logging.debug(f'User {user.name} was added to DB with ObjectId = {res.inserted_id}')
                else:
                    res = app_context.db_manager.users.update_one({'id': user.id}, {'$inc': {'msg_cnt': 1}})
                    logging.debug(f'Updated info for user {user.name}: msg_cnt = {user_info["msg_cnt"]}')

                return res
            except Exception as e:
                logging.exception(e)

    return wrapper
