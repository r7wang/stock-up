import threading
from collections import defaultdict
from typing import Callable, Dict, Optional, Set, Tuple
from uuid import UUID, uuid4


class ConfigBucket:
    """
    Centralized in-memory store for configuration data. Applications are expected to fetch dynamic configurations from
    the bucket whenever a value is needed, as opposed to caching and reusing the previously found value. For more
    complex interactions where fetching the value is insufficient, use a ConfigReactor and register the reactor with a
    ConfigListener.
    """

    def __init__(self):
        # Maps keys to a tuple of (value, version).
        self._data: Dict[str, Tuple[str, int]] = {}

        # Maps keys to subscription ids.
        self._key_subscriptions: Dict[str, Set[UUID]] = defaultdict(set)

        # Maps subscription ids to a tuple of (key, change handler).
        self._subscriptions: Dict[UUID, Tuple[str, Callable]] = {}

        self._lock = threading.Lock()

    def get_int(self, key: str) -> Optional[int]:
        """Get the value for a given key as an integer

        :param key: Key for the value to be returned.
        :return: Integer that maps to the given key.
        """

        val = self._data.get(key)
        if not val:
            return None
        return int(val[0])

    def get_str(self, key: str) -> Optional[str]:
        """Get the value for a given key as a string

        :param key: Key for the value to be returned.
        :return: String that maps to the given key.
        """

        val = self._data.get(key)
        if not val:
            return None
        return str(val[0])

    def remove(self, key: str) -> None:
        """Removes the value for a given key

        :param key: Key for the value to be removed.
        """

        # TODO: Verify whether or not removal is associated with any versioning metadata. If we end up with
        #       out-of-order callbacks, then it's possible that a delete followed by a put becomes a put followed by a
        #       delete.
        with self._lock:
            if key not in self._data:
                return

            del self._data[key]
        self._invoke_change_handlers(key)

    def subscribe(self, key: str, change_handler: Callable) -> UUID:
        """Ensures that a callback function is invoked when changes are made to a key

        :param key: Trigger for the callback function.
        :param change_handler: Callback function to be invoked.
            Parameters:
                None
            Return:
                None
        :return: Unique subscription id that can be used to unsubscribe.
        """

        subscription_id = uuid4()
        while subscription_id in self._subscriptions:
            subscription_id = uuid4()

        self._subscriptions[subscription_id] = (key, change_handler)
        self._key_subscriptions[key].add(subscription_id)

        return subscription_id

    def unsubscribe(self, subscription_id: UUID) -> None:
        """Callback function for a subscription id is no longer invoked when changes are made to a key

        :param subscription_id: Identifier to unsubscribe.
        """

        if subscription_id not in self._subscriptions:
            return

        key = self._subscriptions[subscription_id][0]
        self._key_subscriptions[key].remove(subscription_id)
        del self._subscriptions[subscription_id]

    def update(self, key: str, val: str, version: int) -> bool:
        """Updates the value for the given key, if the version is greater than the current version

        :param key: Key for the data to be updated.
        :param val: Value associated with the given key.
        :param version: Version associated with the given value.
        :return: Whether or not the data has been updated.
        """

        with self._lock:
            if key in self._data and version <= self._data[key][1]:
                return False

            self._data[key] = (val, version)

        self._invoke_change_handlers(key)
        return True

    def _invoke_change_handlers(self, key: str):
        subscription_ids = self._key_subscriptions[key]
        handlers = list(map(lambda subscription_id: self._subscriptions[subscription_id][1], subscription_ids))
        for handler in handlers:
            # TODO: Consider other alternatives for invoking callbacks without blocking the current thread. There is no
            #       guarantee on callback execution order or concurrency.
            handler()
