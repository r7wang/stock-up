import threading
from typing import Any, Callable, Optional

import websocket

from stock_common.log import logger


class StockQuoteListener:
    """
    Listens for stock quotes. Restarting after stopping is unsupported to simplify signal handling. Otherwise, there's
    the possibility that SIGTERM is ignored if received before the server has even started. Listeners have full
    ownership over the websocket applications they create.
    """

    def __init__(self, api_token: str):
        self._api_token = api_token
        self._app: Optional[websocket.WebSocketApp] = None
        self._lock = threading.Lock()
        self._is_done = False

    def start(self, handler: Callable[[str], None]) -> None:
        """Starts listening for stock quotes if the listener has never been stopped

        This call is thread-safe.

        :param handler: Callback function invoked for every message with the following signature:
            message: str
            return: None
        """

        while self._lock_operation(self._setup, handler):
            self._app.run_forever()
            self._lock_operation(self._teardown)

    def stop(self) -> None:
        """Stops the listener permanently

        This call is thread-safe.
        """

        self._lock_operation(self._teardown, is_done=True)

    def _lock_operation(self, func: Callable, *args, **kwargs) -> Any:
        self._lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            self._lock.release()

    def _setup(self, handler: Callable[[str], None]) -> bool:
        """Sets up the listener websocket application.

        This call is not thread-safe and must be wrapped by _lock_operation().

        :param handler: Callback function invoked for every message with the following signature:
            message: str
            return: None
        :return: Whether or not the current thread is allowed to continue operating the listener.
        """

        def _on_message(ws, message):
            handler(message)

        def _on_error(ws, error):
            logger.error(error)

        def _on_close(ws):
            logger.info("Closing websocket...")

        def _on_open(ws):
            ws.send('{"type":"subscribe","symbol":"AMZN"}')

        # May occur if we've signaled the listener to stop before even starting the listener.
        if self._is_done:
            return False

        # May occur if we try to start the listener from multiple threads. Because the application is already being
        # started on another thread, we cannot duplicate this work.
        if self._app:
            return False

        websocket.enableTrace(True)
        self._app = websocket.WebSocketApp(
            "wss://ws.finnhub.io?token={}".format(self._api_token),
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
        if is_done:
            self._is_done = True

        if not self._app:
            return

        self._app.close()
        self._app = None
