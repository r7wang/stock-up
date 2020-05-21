from collections import Callable


class StockQuoteListener:

    def start(self, handler: Callable) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        raise NotImplementedError()
