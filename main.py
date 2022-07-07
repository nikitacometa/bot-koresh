import atexit
import logging
import re
from time import sleep

import requests

from bs4 import BeautifulSoup
from telegram.ext import MessageHandler, Filters

from app.bot.commands.aneks import fix_emojis
from app.bot.commands.commands import Commands
from app.bot.commands.default_handler import default_message_handler
from app.bot.context import app_context

# TODO: make him inline to have an ability to use it in every conversation
# TODO: separate class
from app.bot.settings import PROXIES
from app.bot.updater import run_info_updater_if_not


def get_aneks():
    # TODO: fix aneks
    return # " lol"

    print('lets get some ankes')
    base_url = "https://vk.com/baneksbest?w=wall-85443458_"
    last_id = 32511
    for i in range(30050, last_id + 1):
        try:
            print(f'GET {base_url}{i}')
            response = requests.get(f'{base_url}{i}')
            emoji_reg = r'^<img alt="🚂." class="emoji" src="/emoji/e/.+"/>$'
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                divs = soup.find_all('div')
                aneks = [div for div in divs if div.get('class') == ['wi_body']]
                if len(aneks) == 0:
                    continue
                anek = aneks[0].div
                # print(anek.contents)
                base = anek.prettify()
                good = fix_emojis(base)
                anek_lines = good.replace('<br/>\n', ' ').split('\n')[1:-2]
                text = '\n'.join(anek_lines)
                # print(f'\n\n{text}\n\n')
                f = open(f'aneks/anek{i}.txt', 'w+')
                f.write(text)
                f.close()
                # do not overload the net
                sleep(2)
            else:
                print(f'\n\n\n\n\nshit happens\n\n\n\n\n{response.text}')

        except Exception as e:
            print(e)

def run():
    updater = app_context.updater
    dp = updater.dispatcher

    for command in Commands.get_all():
        command.update_dispatcher(dp)

    # fallback
    dp.add_handler(MessageHandler(Filters.all, default_message_handler))

    updater.start_polling()

    run_info_updater_if_not()

    logging.info('Bot started!\n\nWell... Hello (:\n')

    get_aneks()

    updater.idle()


def tear_down():
    logging.info('EXIT BOT\n\nBye!\n')


if __name__ == '__main__':
    atexit.register(tear_down)

    try:
        run()
    except Exception as ex:
        logging.exception(ex)
