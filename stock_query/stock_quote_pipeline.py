import json
from decimal import Decimal
from typing import List

from stock_common.logging import Logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_writer import StockQuoteWriter


class StockQuotePipeline:
    def __init__(self, writer: StockQuoteWriter):
        self._writer = writer
        self._logger = Logger(type(self).__name__)

    def handler(self, message: str) -> None:
        """Callback that receives a raw stock quote message.

        :param message: Raw stock quote message.
        """

        self._logger.debug(message)
        quotes = self.parse(message)
        self._writer.write(quotes)

    def parse(self, message: str) -> List[StockQuote]:
        """Converts raw stock quote message into their domain representation.

        :param message: Raw stock quote message.
        :return: List of StockQuote objects. Can be empty.
        """

        try:
            # Ensures that we don't lose any precision while loading the JSON.
            data = json.loads(message, parse_float=lambda val: Decimal(val))
        except json.decoder.JSONDecodeError:
            self._logger.error('unknown message: {}'.format(message))
            return []

        message_type = data.get('type')
        if not message_type:
            self._logger.error('message missing type: {}'.format(data))
            return []

        if data.get('type') == 'ping':
            return []

        if not data.get('data'):
            self._logger.error('message missing data: {}'.format(data))
            return []

        quotes = data['data']
        return list(map(
            # Ensure that we always maintain correct data types.
            lambda quote: StockQuote(
                timestamp=int(quote['t']),
                symbol=str(quote['s']),
                price=Decimal(quote['p']),
                volume=int(quote['v']),
            ),
            quotes,
        ))
