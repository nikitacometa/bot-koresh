import re
from typing import List, Tuple, Optional

from telegram import Update
from telegram.ext import CallbackContext

from app.bot.context import app_context
from app.utils.classes.moshnar_command import moshnar_command

COORD_MATCHER = re.compile(r'\d\d\.\d{5,7}\s*,?\s*\d\d\.\d{5,7}')


def extract_coordinates(tokens: List[str]) -> Optional[Tuple[float, float]]:
    all_str = ''.join(tokens)
    match_o = COORD_MATCHER.search(all_str)
    if not match_o:
        return None

    coord_str = match_o.group(0)
    coords = coord_str.split(',') if ',' in coord_str else coord_str.split()
    return float(coords[0]), float(coords[1])


@moshnar_command
def show_map(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        # TODO: show the whole city
        pass
    else:
        coordinates = extract_coordinates(context.args)
        img_link = app_context.map_client.get_img_link_by_coordinates(coordinates)
        update.message.reply_photo(photo=img_link)
