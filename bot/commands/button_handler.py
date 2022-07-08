import logging
from datetime import datetime

from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from bot.context import app_context
from model.challenge import Winner
from utils.callback_context_utils import get_chat_data


CONNECTION_DELAY = 1.5


def try_handle_challenge(query: CallbackQuery, context: CallbackContext) -> bool:
    text = query.data
    if not text.startswith('-') and not text.startswith('+'):
        return False

    action, challenge_id = text.split()

    challenge = get_chat_data(context, 'challenges', {}).get(int(challenge_id))
    if challenge is None:
        logging.error(f'Challenge {challenge_id} is not found...')
        return True

    player = f'@{query.from_user.username}'
    now = datetime.now()

    if action == '+':
        if player in challenge.winners:
            challenge.winners[player].push_cnt += 1
        else:
            spent = now - challenge.started_at
            challenge.winners[player] = Winner(player, spent)
    else:
        if player in challenge.winners:
            del challenge.winners[player]
            challenge.traitors.add(player)
        else:
            logging.info(f'User {player} is not a winner')
            return True

    challenge.post_update(app_context.bot)

    return True


def button_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query

        query.answer()

        if try_handle_challenge(query, context):
            return

    except Exception as e:
        logging.exception(e)

