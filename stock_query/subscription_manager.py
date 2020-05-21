import threading
from typing import Set

from stock_common.config import ConfigBucket
from stock_common.logging import Logger
from stock_query.stock_quote_listener import StockQuoteListener

CONFIG_KEY_SUBSCRIPTIONS = 'subscriptions'


class SubscriptionManager:

    def __init__(self, listener: StockQuoteListener, bucket: ConfigBucket):
        self._listener = listener
        self._bucket = bucket
        self._thread = None
        self._notify_signal = threading.Semaphore(value=0)
        self._current_subs = set()
        self._logger = Logger(type(self).__name__)

    def notify_change(self):
        """Notifies the subscription manager that requested subscriptions have been changed"""

        self._logger.info('notify subscription change')
        self._notify_signal.release()

    def notify_reset(self):
        """Notifies the subscription manager that active subscriptions have been reset"""

        self._logger.info('notify subscription reset')
        self._current_subs.clear()
        self._notify_signal.release()

    def start(self):
        """Starts the subscription manager on a new thread"""

        if self._thread:
            return

        self._logger.info('starting thread')
        self._thread = threading.Thread(target=self._update_subscriptions)
        self._thread.start()

    def stop(self):
        """Stop the subscription manager thread and wait for it to terminate"""

        if not self._thread:
            return

        self._logger.info('stopping thread')
        self._notify_signal.release()
        self._thread.join()

    def _parse_subscriptions(self) -> Set[str]:
        return set(self._bucket.get_str(CONFIG_KEY_SUBSCRIPTIONS).split(','))

    def _update_subscriptions(self) -> None:
        self._logger.info('watching subscriptions')
        subscription_id = self._bucket.subscribe(CONFIG_KEY_SUBSCRIPTIONS, self.notify_change)

        current_subs = set()
        while True:
            self._notify_signal.acquire()

            # Check for completion before making any subscription changes. This prevents exceptions caused by
            # subscriptions that happen after the listener has already been closed.
            if self._listener.is_done():
                break

            requested_subs = self._parse_subscriptions()
            to_add = requested_subs.difference(current_subs)
            to_remove = current_subs.difference(requested_subs)
            self._listener.modify_subscriptions(to_add, to_remove)

            current_subs = requested_subs

        self._logger.info('unwatching subscriptions')
        self._bucket.unsubscribe(subscription_id)
