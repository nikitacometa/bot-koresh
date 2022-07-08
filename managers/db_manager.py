from dataclasses import dataclass
from functools import cached_property

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


@dataclass
class DBManager:
    host: str
    port: int

    @cached_property
    def client(self) -> MongoClient:
        return MongoClient(host=self.host, port=self.port)

    @cached_property
    def db(self) -> Database:
        return self.client.koresh

    @cached_property
    def users(self) -> Collection:
        return self.db.get_collection('users')

    @cached_property
    def trackings(self) -> Collection:
        return self.db.get_collection('trackings')
