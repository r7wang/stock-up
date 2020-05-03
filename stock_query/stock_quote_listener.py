import threading
from typing import Callable, Optional

import websocket

from stock_common.log import logger


class StockQuoteListener:
    """
    Listens for stock quotes. Stopping and restarting is unsupported to simplify signal handling. Otherwise, there's
    the possibility that SIGTERM is ignored if received before the server has even started. Listeners have full
    ownership over the WebSocket applications they create.
    """

    def __init__(self, api_token: str):
        self._api_token = api_token
        self._app: Optional[websocket.WebSocketApp] = None
        self._lock = threading.Lock()
        self._is_done = False

    def start(self, handler: Callable[[str], None]) -> None:
        """Starts listening for stock quotes if the listener has never been stopped

        :param handler: Callback function invoked for every message.
        """

        self._lock.acquire()
        try:
            if self._is_done or self._app:
                return

            self._app = self._build(handler)
        finally:
            self._lock.release()

        self._app.run_forever()

    def stop(self) -> None:
        """Stops the listener permanently"""

        self._lock.acquire()
        try:
            self._is_done = True
            if not self._app:
                return

            self._app.close()
            self._app = None
        finally:
            self._lock.release()

    def _build(self, handler: Callable[[str], None]) -> websocket.WebSocketApp:
        def _on_message(ws, message):
            handler(message)

        def _on_error(ws, error):
            logger.error(error)

        def _on_close(ws):
            logger.info("Closing websocket...")

        def _on_open(ws):
            ws.send('{"type":"subscribe","symbol":"AMZN"}')

        websocket.enableTrace(True)
        return websocket.WebSocketApp(
            "wss://ws.finnhub.io?token={}".format(self._api_token),
            on_open=_on_open,
            on_message=_on_message,
            on_error=_on_error,
            on_close=_on_close,
        )
