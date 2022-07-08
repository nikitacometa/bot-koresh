from datetime import timedelta, datetime
from typing import List, Optional

from env import CONFIRMATIONS_NEEDED
from model.emojis import Emojis
from model.tracking import TransactionInfo


TX_HASH_FOOTPRINT_SIZE = 20
ADDRESS_HASH_FOOTPRINT_SIZE = 15


def unit_to_str(count: int, one: str, no_one: str, no_many: str) -> str:
    if count % 10 == 1:
        return f'{count} {one}'
    if 2 <= count % 10 <= 4:
        return f'{count} {no_one}'
    return f'{count} {no_many}'


def tries_to_str(count: int) -> str:
    return unit_to_str(count, 'раз', 'раза', 'раз')


def days_to_str(count: int) -> str:
    return unit_to_str(count, 'день', 'дня', 'дней')


def hours_to_str(count: int) -> str:
    return unit_to_str(count, 'час', 'часа', 'часов')


def minutes_to_str(count: int) -> str:
    return unit_to_str(count, 'минута', 'минуты', 'минут')


def seconds_to_str(count: int) -> str:
    return unit_to_str(count, 'секунда', 'секунды', 'секунд')


def timedelta_to_str(t: timedelta) -> str:
    res = ''
    if t.days > 0:
        res = days_to_str(t.days)

    hours = t.seconds // 3600
    if hours > 0:
        res += ' ' + hours_to_str(hours)

    minutes = (t.seconds - hours * 3600) // 60
    if minutes > 0:
        res += ' ' + minutes_to_str(minutes)

    seconds = t.seconds - hours * 3600 - minutes * 60
    if seconds > 0:
        res += ' ' + seconds_to_str(seconds)

    return res.strip()


def parse_time_to_seconds(token: str) -> Optional[int]:
    if len(token) == 0 or token[0] != '$':
        return None

    token = token[1:]
    name = token[-1]
    num_str = token[:-1]

    try:
        num = int(num_str)
    except Exception:
        return None

    res = None

    if name == 's':
        res = num

    if name == 'm':
        res = num * 60

    if name == 'h':
        res = num * 60 * 60

    if name == 'd':
        res = num * 60 * 60 * 24

    return res


def parse_time(token: str) -> Optional[timedelta]:
    seconds = parse_time_to_seconds(token)
    return timedelta(seconds=seconds) if seconds is not None else None


def datetime_to_str(d: datetime) -> str:
    return d.strftime('%H:%M:%S')


def get_addr_url(addr: str) -> str:
    return f'https://www.blockchain.com/btc/address/{addr}'


def get_addr_html_url(addr: str) -> str:
    return f'<a href=\'{get_addr_url(addr)}\'>{addr[:ADDRESS_HASH_FOOTPRINT_SIZE]}...</a>'


def get_addr_list_html_str(addrs: List[str]) -> str:
    return '\n'.join(map(get_addr_html_url, addrs))


def tx_info_to_str(info: TransactionInfo) -> str:
    confirmed = Emojis.get_confirmation_status_emoji(info.conf_cnt >= CONFIRMATIONS_NEEDED)
    return f'<code>[{confirmed}][</code><a href=\'{get_tx_url(info.hash)}\'>' \
           f'{info.conf_cnt} confirmations</a><code>]</code>\n' \
           f'<code>[created {datetime_to_str(info.created_at)}]</code>'


def get_tx_url(tx_hash: str) -> str:
    return f'https://www.blockchain.com/btc/tx/{tx_hash}'


def get_tx_url_html_str(tx_hash: str) -> str:
    text = f'{tx_hash[:TX_HASH_FOOTPRINT_SIZE]}...'
    url = get_tx_url(tx_hash)

    return f'<a href=\'{url}\'>{text}</a>'
