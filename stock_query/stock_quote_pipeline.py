import json
from decimal import Decimal
from typing import List

from stock_common.log import logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_writer import StockQuoteWriter


class StockQuotePipeline:
    def __init__(self, writer: StockQuoteWriter):
        self._writer = writer

    def handler(self, message: str) -> None:
        """Callback that receives a raw stock quote message.

        :param message: Raw stock quote message.
        """

        logger.debug(message)
        quotes = self.parse(message)
        self._writer.write(quotes)

    def parse(self, message: str) -> List[StockQuote]:
        """Converts raw stock quote message into their domain representation.

        :param message: Raw stock quote message.
        :return: List of StockQuote objects. Can be empty.
        """

        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            logger.error('Unknown message: {}'.format(message))
            return []

        message_type = data.get('type')
        if not message_type:
            logger.error('Message missing type: {}'.format(data))
            return []

        if data.get('type') == 'ping':
            return []

        if not data.get('data'):
            logger.error('Message missing data: {}'.format(data))
            return []

        quotes = data['data']
        return list(map(
            lambda quote: StockQuote(
                timestamp=quote['t'],
                symbol=quote['s'],
                price=Decimal(quote['p']),
                volume=quote['v'],
            ),
            quotes,
        ))
