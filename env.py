import logging
import os
import sys
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

from pydantic import BaseSettings

VERSION = '1.5.0'

PROXY_URL = 'socks5h://localhost:9050'
PROXIES = dict(http=PROXY_URL, https=PROXY_URL)

# TODO: try more often
TRACKINGS_UPDATE_INTERVAL = timedelta(seconds=30)
# TODO: make request argument
CONFIRMATIONS_NEEDED = 1

# TODO: configure per chat
SLADKO_EVERY_N = 250

MAX_USER_PHOTOS = 13
SAVE_LAST_MESSAGES_CNT = 10

COMMAND_RETRIES = 2
TRACKING_TTL = timedelta(hours=3)

LOGGING_LEVEL = logging.DEBUG
TELEGRAM_API_LOGGING_LEVEL = logging.INFO

LOGS_DIR = f'{os.getcwd()}/.logs'
print(f'Logs are at {LOGS_DIR}')


class Settings(BaseSettings):
    # Proxy
    enable_proxy: bool
    proxy_bot_updates: bool

    # APIs
    tg_api_token: str
    translator_api_key: str

    # DB
    mongodb_host: str
    mongodb_port: int

    # CHATS
    bot_chat_id: int
    admin_chat_id: int

    # Disk
    storage_dir: str

    # Bot
    hi_mark_delay_h: int

    class Config:
        env_file = '.env'
        arbitrary_types_allowed = True

    @property
    def hi_mark_delay(self) -> timedelta:
        return timedelta(hours=self.hi_mark_delay_h)

    def proxies(self):
        return PROXIES if self.enable_proxy else None


def setup_logging():
    os.makedirs(LOGS_DIR, exist_ok=True)
    # 10000 here means infinity
    rotating_file_handler = TimedRotatingFileHandler(f'{LOGS_DIR}/bot.log', backupCount=10000, when='D', interval=1)
    console_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%I:%M:%S',
        level=LOGGING_LEVEL,
        **{'handlers': [console_handler, rotating_file_handler]}
    )

    logging.getLogger('telegram').setLevel(TELEGRAM_API_LOGGING_LEVEL)
    logging.getLogger('JobQueue').setLevel(TELEGRAM_API_LOGGING_LEVEL)

    logging.getLogger('telegram.ext.dispatcher').setLevel(LOGGING_LEVEL)


settings = Settings()

setup_logging()
os.makedirs(settings.storage_dir, exist_ok=True)
