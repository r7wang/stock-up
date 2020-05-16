from typing import List

from stock_common.stock_quote import StockQuote
from stock_query.deduplication_cache import DeduplicationCache
from stock_query.stock_quote_producer import StockQuoteProducer


class StockQuoteWriter:
    """
    Writes stock quotes to a stock quote producer.
    """

    def __init__(self, producer: StockQuoteProducer):
        self._producer = producer
        self._dedup_cache = DeduplicationCache()

    def write(self, quotes: List[StockQuote]) -> None:
        for quote in quotes:
            if self._dedup_cache.is_duplicate(quote):
                continue

            # TODO: If the retry fails because Kafka/RMQ is not ready to accept connections, then we should add the
            #       message to a buffer.
            self._producer.send(quote)
