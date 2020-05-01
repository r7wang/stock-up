from typing import Dict, List

from stock_query.stock_quote import StockQuote


class StockQuoteParser:
    def read(self, data: Dict) -> List[StockQuote]:
        message_type = data.get('type')
        if not message_type:
            print('Message missing type: {}'.format(data))
            return []

        if data.get('type') == 'ping':
            return []

        if not data.get('data'):
            print('Message missing data: {}'.format(data))
            return []

        quotes = data['data']
        return list(map(
            lambda quote: StockQuote(
                timestamp=quote['t'],
                symbol=quote['s'],
                price=quote['p'],
                volume=quote['v'],
            ),
            quotes,
        ))
