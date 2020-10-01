import copy
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import cached_property
from typing import Optional, List, Dict

from pymongo.collection import Collection

from app.external.blockchain_client import BlockchainClient
from app.managers.db_manager import DBManager
from app.model.tracking import Tracking, AddressStatus, TransactionInfo


# TODO: schedule backups
@dataclass
class TrackingManager:
    blockchain_client: BlockchainClient
    db_manager: DBManager

    @cached_property
    def db(self) -> Collection:
        return self.db_manager.trackings

    @cached_property
    def trackings_by_hash(self) -> Dict[str, Tracking]:
        return {t.address: t for t in self.get_all()}

    def get_all(self) -> List[Tracking]:
        return list(Tracking.from_dict(d) for d in self.db.find({}) if d is not None)

    def get_by_chat_id(self, chat_id: int) -> List[Tracking]:
        return list(Tracking.from_dict(d) for d in self.db.find({'chat_id': chat_id}) if d is not None)

    def create(self, address: str, chat_id: int, status: AddressStatus, transactions: List[TransactionInfo]):
        now = datetime.now()
        new_tracking = Tracking(address, chat_id, now, status, now, transactions)
        res = self.db.insert_one(asdict(new_tracking))
        if not res.acknowledged:
            return None

        return new_tracking

    def update_tracking(self, t: Tracking) -> Tracking:
        updated = copy.deepcopy(t)
        now = datetime.now()

        # TODO: update every tx separately
        status, tx_info = self.blockchain_client.check_address(t.address)
        if status == AddressStatus.CHECK_FAILED:
            return updated

        additional_info_str = f', {tx_info.conf_cnt} confirmations' if status.has_transaction() else ''
        logging.debug(f'--> {t.address} in state {status}{additional_info_str}')

        if status != t.status:
            res = self.db.update_one({'address': t.address}, {'$set': {'status': status}})
            if res.modified_count == 0:
                logging.error(f'Failed to update status for address {t.address}')
                return updated
            updated.status = status

        # TODO: fix bug with null in transactions array
        if tx_info:
            found = False
            for tx in updated.transactions:
                if tx.hash == tx_info.hash:
                    found = True
                    if tx.conf_cnt != tx_info.conf_cnt:
                        tx.conf_cnt = tx_info.conf_cnt
                        tx.updated_at = tx_info.updated_at
                        logging.debug(f'{tx.conf_cnt} -> {tx_info.conf_cnt}')
                        self.db.update_one(
                            {'transactions.hash': tx.hash},
                            {'$set': {'transactions.$.conf_cnt': tx_info.conf_cnt,
                                      'transactions.$.updated_at': tx_info.updated_at}
                             }
                        )

            if not found:
                updated.transactions.append(tx_info)
                # TODO: refactor same code
                self.db.update_one(
                    {'address': t.address},
                    {'$push': {'transactions': asdict(tx_info)}}
                )

        self.db.update_one({'address': t.address}, {'$set': {'updated_at': now}})
        self.trackings_by_hash[t.address] = updated

        return updated

    def remove_tracking(self, t: Tracking) -> bool:
        res = self.db.delete_one({'address': t.address})
        if res.deleted_count > 0:
            if t.address in self.trackings_by_hash:
                del self.trackings_by_hash[t.address]
            return True
        return False

    def has_tracking_for_address(self, address: str) -> bool:
        return address in self.trackings_by_hash

    def get_tracking_by_address(self, address: str) -> Optional[Tracking]:
        return self.trackings_by_hash.get(address)
