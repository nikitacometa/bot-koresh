import os
import random
from time import sleep

import requests
from bs4 import BeautifulSoup

ANEK_DIR = 'aneks'


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


def get_anek() -> str:
    files = os.listdir(ANEK_DIR)
    print(f'Total {len(files)} aneks')
    if len(files) == 0:
        return 'Твоя жизнь как анек, братишка'

    anek_name = f'{ANEK_DIR}/{random.choice(files)}'
    with open(anek_name, 'r') as f:
        return fix_emojis(f.read())


def fetch_aneks():
    base_url = 'https://baneks.ru/'
    first_id = 1
    last_id = 1300

    print(f'lets get some aneks from {base_url}')

    for i in range(first_id, last_id + 1):
        try:
            print(f'#{i} GET {base_url}{i}')
            response = requests.get(f'{base_url}{i}')

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # print(soup.prettify())
                # print('\n\n\n\n')

                metas = soup.find_all('meta')
                # for meta in metas:
                #     print('\n')
                #     print(meta.get('name'))
                #     print(meta)

                aneks = [meta for meta in metas if meta.get('name') == 'description']
                if len(aneks) == 0:
                    print('zero')
                    continue

                anek = aneks[0].get('content')
                print('anek')
                print(anek)
                # print('||||||')

                # base = anek.prettify()
                # good = fix_emojis(base)
                # anek_lines = good.replace('<br/>\n', ' ').split('\n')[1:-2]
                # text = '\n'.join(anek_lines)
                # print(f'{text}\n\n')

                with open(f'{ANEK_DIR}/{i}.txt', 'w+') as f:
                    f.write(anek)

                # do not overload the net
                sleep(1)
            else:
                print(f'\n\n\n\n\nshit happens\n\n\n\n\n{response.text}')

        except Exception as e:
            print(e)
