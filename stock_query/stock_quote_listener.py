import threading
from typing import Callable, Optional, Set

import websocket

from stock_common.logging import Logger


class StockQuoteListener:
    """
    Listens for stock quotes. Restarting after stopping is unsupported to simplify signal handling. Otherwise, there's
    the possibility that SIGTERM is ignored if received before the server has even started. Listeners have full
    ownership over the websocket applications they create.
    """

    def __init__(self, api_token: str):
        self._api_token = api_token
        self._app: Optional[websocket.WebSocketApp] = None
        # Lock to synchronize setup/teardown of the websocket application.
        self._ws_lock = threading.Lock()
        self._is_done = False
        self._logger = Logger(type(self).__name__)

    def is_done(self) -> bool:
        return self._is_done

    def start(self, open_handler: Callable, message_handler: Callable) -> None:
        """Starts listening for stock quotes if the listener has never been stopped

        This call is thread-safe.

        :param open_handler: Callback function invoked when the websocket connection is ready.
            Parameters:
                None
            Return:
                None
        :param message_handler: Callback function invoked for every message.
            Parameters:
                message: str
            Return:
                None
        """

        while self._setup(open_handler, message_handler):
            self._app.run_forever()
            self._teardown()

    def stop(self) -> None:
        """Stops the listener permanently

        This call is thread-safe.
        """

        self._teardown(is_done=True)

    def modify_subscriptions(self, to_add: Set[str], to_remove: Set[str]) -> None:
        """Modifies subscriptions

        This call is thread-safe.

        :param to_add: Subscriptions to be add.
        :param to_remove: Subscriptions to be removed.
        """

        # Prevent any operations that modify the state of the websocket while messages are actively being sent.
        with self._ws_lock:
            # Websocket application may not be ready to accept commands if unreliable connection is still being
            # reinitialized.
            if not self._app:
                return

            for symbol in to_add:
                self._logger.info('subscribing to {}'.format(symbol))
                self._app.send('{{"type":"subscribe","symbol":"{}"}}'.format(symbol))
            for symbol in to_remove:
                self._logger.info('unsubscribing from {}'.format(symbol))
                self._app.send('{{"type":"unsubscribe","symbol":"{}"}}'.format(symbol))

    def _setup(self, open_handler: Callable, message_handler: Callable) -> bool:
        """Sets up the listener websocket application

        This call is not thread-safe and must be wrapped by _lock_operation().

        :param open_handler: Callback function invoked when the websocket connection is ready.
            Parameters:
                None
            Return:
                None
        :param message_handler: Callback function invoked for every message.
            Parameters:
                message: str
            Return:
                None
        :return: Whether or not the current thread is allowed to continue operating the listener.
        """

        def _on_open(app: websocket.WebSocketApp):
            self._logger.info('websocket opened')
            open_handler()

        def _on_message(app: websocket.WebSocketApp, message: str):
            message_handler(message)

        def _on_error(app: websocket.WebSocketApp, error):
            # TODO: We may want to handle specific errors here and restart the websocket connection.
            #       ERROR Handshake status 502 Bad Gateway
            self._logger.error(error)

        def _on_close(app: websocket.WebSocketApp):
            self._logger.info('websocket closed')

        with self._ws_lock:
            # May occur if we've signaled the listener to stop before even starting the listener.
            if self._is_done:
                return False

            # May occur if we try to start the listener from multiple threads. Because the application is already being
            # started on another thread, we cannot duplicate this work.
            if self._app:
                return False

            websocket.enableTrace(True)
            self._app = websocket.WebSocketApp(
                'wss://ws.finnhub.io?token={}'.format(self._api_token),
                on_open=_on_open,
                on_message=_on_message,
                on_error=_on_error,
                on_close=_on_close,
            )
            return True

    def _teardown(self, is_done: bool = False) -> None:
        """Tears down the listener websocket application.

        This call is not thread-safe and must be wrapped by _lock_operation().

        :param is_done: If true, flag the listener to be permanently stopped.
        """

        with self._ws_lock:
            if is_done:
                self._is_done = True

            if not self._app:
                return

            self._app.close()
            self._app = None
