from stock_common.log import logger
from stock_query.stock_quote_listener import StockQuoteListener
from stock_query.stock_quote_reader import StockQuoteReader
from stock_query.stock_quote_writer import StockQuoteWriter


class Server:
    def __init__(
        self,
        stock_quote_listener: StockQuoteListener,
        stock_quote_reader: StockQuoteReader,
        stock_quote_writer: StockQuoteWriter,
    ):
        self._listener = stock_quote_listener
        self._reader = stock_quote_reader
        self._writer = stock_quote_writer

    def start(self) -> None:
        self._listener.start(self._process_stock_quote)

    def stop(self) -> None:
        self._listener.stop()

    def _process_stock_quote(self, message: str) -> None:
        logger.debug(message)
        quotes = self._reader.read(message)
        self._writer.write(quotes)
