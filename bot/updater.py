import logging
from typing import Optional, List

from telegram.ext import CallbackContext, Job

from bot.context import app_context, settings
from env import TRACKING_TTL
from managers.phrase_manager import PhraseManager
from model.tracking import AddressStatus, TransactionInfo
from utils.message_utils import send_tx_info


def transactions_changed(old_txs: List[TransactionInfo], new_txs: List[TransactionInfo]) -> bool:
    if len(old_txs) != len(new_txs):
        return True

    old_txs = sorted(old_txs, key=lambda tx: tx.hash)
    new_txs = sorted(new_txs, key=lambda tx: tx.hash)

    return any(old.hash != new.hash or old.conf_cnt != new.conf_cnt for old, new in zip(old_txs, new_txs))


def update_trackings(context: CallbackContext):
    logging.debug('-> Updating trackings...')

    try:
        for t in app_context.tracking_manager.get_all():
            # TODO: optimize checking for any tx update
            updated = app_context.tracking_manager.update_tracking(t)

            if updated.status != t.status:
                if updated.status == AddressStatus.NOT_CONFIRMED:
                    send_tx_info(updated, 'Так-то опачи))')
                    continue

                if updated.status == AddressStatus.CONFIRMED:
                    send_tx_info(updated, PhraseManager.just_confirmed_reaction())
                    if app_context.tracking_manager.remove_tracking(updated):
                        logging.debug(f'Address {updated.address} was removed.')
                    else:
                        logging.debug(f'Failed to remove address {updated.address}.')
                    continue

            if updated.status == AddressStatus.NOT_CONFIRMED and transactions_changed(t.transactions, updated.transactions):
                send_tx_info(updated, 'Так-с так-с так-с што тут у н а с ) )  (хех плотный лол)')
                continue

            if updated.age > TRACKING_TTL:
                if app_context.tracking_manager.remove_tracking(updated):
                    logging.debug(f'Address {updated.address} was removed.')
                else:
                    logging.debug(f'Failed to remove address {updated.address}.')
                continue

    except Exception as e:
        logging.exception(e)

    logging.debug('-> Updating done.')


def run_info_updater_if_not() -> Optional[Job]:
    if app_context.updater_job is None:
        app_context.updater_job = app_context.job_queue.run_repeating(callback=update_trackings, interval=settings)
    return app_context.updater_job
