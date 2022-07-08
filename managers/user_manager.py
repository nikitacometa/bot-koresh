from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from pymongo.collection import Collection

from managers.db_manager import DBManager
from model.user import User, FileInfo


@dataclass
class UserManager:
    db_manager: DBManager

    @cached_property
    def users(self) -> Collection:
        return self.db_manager.users

    def create(self, user_id: int, user_name: str, msg_cnt: int = 0) -> Optional[User]:
        new_user = User(user_id, user_name, msg_cnt)
        res = self.users.insert_one(new_user.to_json())
        return new_user if res.acknowledged else None

    def get(self, user_id: int) -> Optional[User]:
        user_dict = self.users.find_one({'id': user_id})
        return User.from_dict_o(user_dict)

    def get_or_create(self, user_id: int, user_name: str, msg_cnt: int = 0) -> User:
        user = self.get(user_id=user_id)
        return user if user is not None else self.create(user_id, user_name, msg_cnt)

    def update_user_with_new_file(self, user: User, file_info: FileInfo) -> Optional[User]:
        user.stored_files.append(file_info)
        res = self.users.update_one({'id': user.id}, {'$set': {'stored_files': user.stored_files}})
        if res.modified_count == 0:
            return None
        return user
