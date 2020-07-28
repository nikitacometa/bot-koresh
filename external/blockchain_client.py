import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple, Optional, Dict, ClassVar

import requests

from bot.settings import CONFIRMATIONS_NEEDED, PROXIES
from model.tracking import AddressStatus, TransactionInfo

from bot.validator import is_valid_bitcoin_address


@dataclass
class BlockchainClient:
    BASE_URL: ClassVar[str] = 'https://blockchain.info'

    _cache: Dict[str, TransactionInfo] = field(default_factory=dict)

    def get_last_tx_info(self, address: str) -> Optional[TransactionInfo]:
        if not is_valid_bitcoin_address(address):
            logging.exception(f'Invalid bitcoin address: {address}')
            return None

        # TODO: check if too old
        if address in self._cache:
            return self._cache[address]

        response = requests.get(f'{self.BASE_URL}/rawaddr/{address}', proxies=PROXIES)
        if response.status_code != 200:
            return None

        address_info = response.json()
        if address_info['n_tx'] == 0:
            return None

        last_transaction = address_info['txs'][0]
        self._cache[address] = self._get_tx_info(last_transaction)
        return self._cache[address]

    def check_address(self, address: str) -> Tuple[AddressStatus, Optional[TransactionInfo]]:
        if not is_valid_bitcoin_address(address):
            logging.error(f'Invalid bitcoin address: {address}')
            return AddressStatus.INVALID_HASH, None

        logging.debug(f'get --> {address}')
        response = requests.get(f'{self.BASE_URL}/rawaddr/{address}', proxies=PROXIES)
        now = datetime.now()

        # TODO: restart tor
        if response.status_code == 429:
            logging.error(f'{response.headers}')
        if response.status_code != 200:
            logging.error(f'Failed to check {address}')
            return AddressStatus.CHECK_FAILED, None

        address_info = response.json()
        if address_info['n_tx'] == 0:
            return AddressStatus.NO_TRANSACTIONS, None

        # TODO: return list of all unconfirmed txs
        last_transaction = address_info['txs'][0]
        tx_info = self._get_tx_info(last_transaction, now)

        if tx_info.conf_cnt is None:
            return AddressStatus.CHECK_FAILED, None

        if tx_info.conf_cnt >= CONFIRMATIONS_NEEDED:
            return AddressStatus.CONFIRMED, tx_info
        else:
            return AddressStatus.NOT_CONFIRMED, tx_info

    def get_confirmations_count(self, tx: str) -> Optional[int]:
        response = requests.get(f'{self.BASE_URL}/rawtx/{tx}', proxies=PROXIES)
        if response.status_code != 200:
            logging.error(f'Failed to fetch transaction {tx} info')
            return None

        transaction_info = response.json()
        block_height = transaction_info.get('block_height')
        if block_height is None:
            return 0

        response = requests.get(f'{self.BASE_URL}/q/getblockcount', proxies=PROXIES)
        if response.status_code != 200:
            logging.error(f'Failed to fetch total number of blocks')
            return None

        total_blocks = response.json()

        return total_blocks - block_height + 1

    def _get_tx_info(self, last_transaction: Dict[str, str], updated_at: datetime) -> TransactionInfo:
        tx_hash = last_transaction['hash']
        tx_created_at = datetime.fromtimestamp(int(last_transaction['time']))
        confirmations_cnt = self.get_confirmations_count(tx_hash)
        return TransactionInfo(tx_hash, tx_created_at, confirmations_cnt, updated_at)

    def get_unconfirmed_txs(self):
        response = requests.get(f'{self.BASE_URL}/unconfirmed-transactions?format=json', proxies=PROXIES)
        res = response.json()['txs']

        logging.debug(f'{len(res)} unconfirmed txs in total')

        return res

    def get_last_unconfirmed_tx(self):
        res = self.get_unconfirmed_txs()[-1]

        logging.debug(f'last_unconfirmed_tx = {res}')

        return res

    def get_random_address_with_unconfirmed_tx(self) -> Optional[str]:
        last_tx = self.get_last_unconfirmed_tx()
        return next(filter(None, (out.get('addr', None) for out in last_tx.get('out', {}))), None)
