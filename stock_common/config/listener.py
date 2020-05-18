import re
from typing import Optional, List, Dict

import etcd3
from etcd3 import Etcd3Client
from etcd3.events import Event, PutEvent, DeleteEvent
from etcd3.watch import WatchResponse

from stock_common.config import ConfigBucket, ConfigReactor
from stock_common.logging import logger


class ConfigListener:
    def __init__(self, config_server: str, base_prefix: str, reactors: Dict[str, ConfigReactor]):
        self._config_server = config_server
        self._base_prefix = base_prefix
        self._reactors = reactors
        self._client: Optional[Etcd3Client] = None
        self._watch_id = None
        self._pattern = re.compile('^{}/(.*)'.format(self._base_prefix))
        self._bucket = ConfigBucket()

    def __enter__(self):
        self._client = etcd3.client(host=self._config_server)
        self._watch_id = self._client.add_watch_prefix_callback(
            key_prefix=self._base_prefix,
            callback=self._on_event,
        )
        for val, metadata in self._client.get_prefix(key_prefix=self._base_prefix):
            self._update_key(metadata.key, val, metadata.version)

    def __exit__(self):
        if self._client and self._watch_id:
            self._client.cancel_watch(self._watch_id)

    def bucket(self) -> ConfigBucket:
        return self._bucket

    def _decode(self, key: bytes) -> str:
        return key.decode('utf-8')

    def _key_suffix(self, key: str) -> Optional[str]:
        """Strip the base prefix from the given key.

        :param key: Fully qualified key.
        :return: Key suffix, without the base prefix.
        """

        match = self._pattern.match(key)
        if not match:
            return None

        return match[1]

    def _on_event(self, response: WatchResponse) -> None:
        """Callback function for watched keys.

        This function is invoked on a separate thread.

        :param response: Contains a response header with metadata and one or more events. Only put and delete events
                         are known and supported.
        """

        events: List[Event] = response.events
        for event in events:
            if isinstance(event, PutEvent):
                self._update_key(event.key, event.value, event.version)
            elif isinstance(event, DeleteEvent):
                self._remove_key(event.key)
            else:
                logger.warn('Config listener could not handle event: type={}'.format(type(event)))

    def _remove_key(self, key: bytes) -> None:
        """Remove the key.

        :param key: Key for the data to be removed.
        """

        str_key = self._key_suffix(self._decode(key))
        self._bucket.remove(key=str_key)

    def _update_key(self, key: bytes, val: bytes, version: int) -> None:
        """Attempt to update the key.

        If the update triggers a change to the underlying data, then signal the appropriate reactors.

        :param key: Key for the data to be updated.
        :param val: Value associated with the given key.
        :param version: Version associated with the given value.
        """

        str_key = self._key_suffix(self._decode(key))
        str_val = self._decode(val)
        modified = self._bucket.update(key=str_key, val=str_val, version=version)
        if modified and str_key in self._reactors:
            logger.info('Config update: {} = {}, version {}'.format(str_key, str_val, version))
            self._reactors[str_key].react(str_val)
