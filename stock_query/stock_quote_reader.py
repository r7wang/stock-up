import json
from decimal import Decimal
from typing import List

from stock_common.log import logger
from stock_common.stock_quote import StockQuote


class StockQuoteReader:
    """
    Readers bridge raw stock quotes with their domain representation.
    """

    def read(self, message: str) -> List[StockQuote]:
        """Converts raw stock quote message into one or more StockQuote objects.

        :param message: Raw stock quote message.
        :return: List of StockQuote objects.
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
