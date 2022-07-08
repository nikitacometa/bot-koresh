import os
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from typing import Optional

from telegram import Bot
from telegram.ext import Updater, Job

from env import Settings, PROXY_URL
from external.blockchain_client import BlockchainClient
from external.map_client import MapClient
from external.translator_client import TranslatorClient
from managers.db_manager import DBManager
from managers.user_manager import UserManager
from managers.tracking_manager import TrackingManager


@dataclass
class Context:
    blockchain_client: BlockchainClient = field(default_factory=BlockchainClient)
    translator_client: TranslatorClient = field(default_factory=TranslatorClient)
    db_manager: DBManager = field(default_factory=DBManager)

    last_hi_mark_at: datetime = field(default=datetime.now() - settings.hi_mark_delay)

    updater_job: Optional[Job] = field(default=None)

    @cached_property
    def settings(self) -> Settings:
        return Settings()

    @cached_property
    def updater(self) -> Updater:
        updater_args = {}
        if self.settings.proxy_bot_updates:
            updater_args['proxy_url'] = PROXY_URL
        return Updater(settings.tg_api_token, use_context=True, request_kwargs=updater_args)

    @cached_property
    def bot(self) -> Bot:
        return self.updater.bot

    @cached_property
    def map_client(self) -> MapClient:
        return MapClient()

    @cached_property
    def tracking_manager(self) -> TrackingManager:
        return TrackingManager(self.blockchain_client, self.db_manager)

    @cached_property
    def user_manager(self) -> UserManager:
        return UserManager(self.db_manager)

    @cached_property
    def job_queue(self):
        return self.updater.job_queue


app_context = Context()
settings = app_context.settings

os.makedirs(settings.storage_dir, exist_ok=True)
