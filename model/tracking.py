import enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict


class TrackingStatus(str, enum.Enum):
    INVALID_HASH = 'invalid_hash'
    NOT_STARTED = 'not_started'
    TRANSACTION_IS_OLD = 'transaction_is_too_old'
    NO_TRANSACTIONS = 'no_transactions'
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    TIMEOUT = 'timeout'
    FAILED = 'failed'
    INTERRUPTED = 'interrupted'

    def has_transaction(self):
        return self == self.NOT_CONFIRMED or self == self.CONFIRMED


@dataclass
class TransactionInfo:
    hash: str
    created_at: datetime
    confirmations_count: int

    @property
    def age(self) -> timedelta:
        return datetime.now() - self.created_at


@dataclass
class Tracking:
    address: str
    added_at: datetime
    chat_id: int

    status: TrackingStatus
    status_updated_at: datetime
    last_tx_confirmations: Optional[int] = None

    def to_dict(self) -> Dict:
        return dict(
            address=f'"{self.address}"',
            added_at=self.added_at.timestamp(),
            chat_id=self.chat_id,
            status=f'"{self.status}"',
            status_updated_at=self.status_updated_at.timestamp()
        )

    def to_json(self) -> str:
        return '{' + ', '.join([f'"{k}": {v}'for (k, v) in self.to_dict().items()]) + '}'
