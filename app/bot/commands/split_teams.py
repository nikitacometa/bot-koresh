import logging
import random
from typing import List, Optional

from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from app.managers.phrase_manager import PhraseManager
from app.utils.classes.moshnar_command import moshnar_command
from app.utils.classes.sending_action import send_action
from app.utils.message_utils import send_message


def split_people(names: List[str], teams_cnt: int) -> List[List[str]]:
    random.shuffle(names)
    names_cnt = len(names)
    res = []
    first = 0
    while teams_cnt > 0:
        size = names_cnt // teams_cnt

        res.append(names[first: first + size])

        names_cnt -= size
        teams_cnt -= 1
        first += size
    return res


@moshnar_command
@send_action(ChatAction.TYPING)
def split_into_teams(update: Update, context: CallbackContext):
    logging.debug('split_teams')

    def is_captains(word: str) -> bool:
        return word.startswith('капитан')

    def get_teams_cnt(s: str) -> Optional[int]:
        teams_cnt_tokens = list(filter(lambda token: token.isnumeric(), s.split()))
        if not teams_cnt_tokens:
            return None
        return int(teams_cnt_tokens[0])

    text = update.message.text

    try:
        if not context.chat_data.get('not_a_command'):
            talk = ''
            names = context.args
        elif ':' in text:
            talk, names_str = text.split(':')
            names = names_str.split()
        else:
            lines = text.split('\n')
            talk = lines[0]
            names = lines[1:]
        context.chat_data['not_a_command'] = False

        # TODO: check team_cnt > players_cnt

        teams_cnt = get_teams_cnt(talk)

        if teams_cnt is None:
            teams_cnt = 2

        if teams_cnt <= 0:
            send_message(context, update, 'Ну это хуйня какая-то сорри')
            return

        if teams_cnt > len(names):
            logging.debug(f'teams_cnt = {teams_cnt}, names_cnt = {len(names)}')

            send_message(context, update, 'Игроков маловато чёт')
            return

        need_generate_captains = any(map(is_captains, talk.split()))

        teams = split_people(names, teams_cnt)
        team_num = 1

        send_message(context, update, PhraseManager.no_problem())
        for team in teams:
            if need_generate_captains:
                captain = random.choice(team)
                team.remove(captain)
                msg = f'Команда #{team_num}\n' + f'{captain} - Капитан\n' + '\n'.join(team) + '\n'
            else:
                msg = f'Команда #{team_num}\n' + '\n'.join(team) + '\n'

            team_num += 1
            send_message(context, update, msg)

    except Exception as e:
        logging.exception(e)


def is_splitting(text: str) -> bool:
    def is_asking(word: str) -> bool:
        return word in ('подели', 'раздели', 'намошни')

    def is_please(word: str) -> bool:
        return word in ('плиз', 'плз', 'пож', 'плез', 'пожалуйста', 'по-братски')

    def matches(s: str) -> bool:
        return any(map(is_asking, s.split())) and any(map(is_please, s.split()))

    return text is not None and matches(text)
