from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from dacite import from_dict
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FileInfo:
    id: str
    telegram_path: str
    local_path: str
    downloaded_at: datetime
    ttl: Optional[timedelta]


@dataclass_json
@dataclass
class User:
    id: int
    name: str
    msg_cnt: int
    stored_files: List[FileInfo] = field(default_factory=list)

    @classmethod
    def from_dict(cls, user_dict: Dict) -> 'User':
        return from_dict(data_class=User, data=user_dict)

    @classmethod
    def from_dict_o(cls, user_dict: Optional[Dict]) -> Optional['User']:
        return from_dict(data_class=User, data=user_dict) if user_dict is not None else None
