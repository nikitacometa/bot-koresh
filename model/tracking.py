import enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from dacite import from_dict
from dataclasses_json import dataclass_json


class AddressStatus(str, enum.Enum):
    INVALID_HASH = 'invalid_hash'
    NO_TRANSACTIONS = 'no_transactions'
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    CHECK_FAILED = 'check_failed'

    def is_not_confirmed(self):
        return self == self.NOT_CONFIRMED

    def is_confirmed(self):
        return self == self.CONFIRMED

    def has_no_transactions(self):
        return self == self.NO_TRANSACTIONS

    def has_transaction(self):
        return self.is_not_confirmed or self.is_confirmed()

    def in_progress(self):
        return self.has_transaction() or self == self.NO_TRANSACTIONS

    def should_continue(self):
        return self.is_not_confirmed() or self.has_no_transactions()


@dataclass_json
@dataclass
class TransactionInfo:
    hash: str
    created_at: datetime
    conf_cnt: int
    updated_at: datetime

    @property
    def age(self) -> timedelta:
        return datetime.now() - self.created_at


@dataclass_json
@dataclass
class Tracking:
    address: str
    chat_id: int
    created_at: datetime
    status: AddressStatus
    updated_at: datetime

    transactions: List[TransactionInfo] = field(default_factory=list)

    @property
    def age(self) -> timedelta:
        return self.updated_at - self.created_at

    @classmethod
    def from_dict(cls, tracking_dict: Dict) -> 'Tracking':
        return from_dict(data_class=Tracking, data=tracking_dict)

    @classmethod
    def from_dict_o(cls, tracking_dict: Optional[Dict]) -> Optional['Tracking']:
        return from_dict(data_class=Tracking, data=tracking_dict) if tracking_dict is not None else None
