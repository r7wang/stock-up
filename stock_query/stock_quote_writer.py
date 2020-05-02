from collections import deque
from typing import List

import kafka
from kafka.errors import KafkaTimeoutError

from stock_common import utils
from stock_query.stock_quote import StockQuote


class StockQuoteWriter:
    """
    Writes stock quotes to a Kafka producer.
    """

    def __init__(self, producer: kafka.KafkaProducer, topic: str):
        self._producer = producer
        self._topic = topic
        self._dedup_cache = deque()
        self._dedup_cache_max_size = 10

    def write(self, quotes: List[StockQuote]) -> None:
        for quote in quotes:
            quote_hash = quote.get_hash()
            if quote_hash in self._dedup_cache:
                continue

            if len(self._dedup_cache) > self._dedup_cache_max_size:
                self._dedup_cache.popleft()
            self._dedup_cache.append(quote_hash)

            utils.retry(
                lambda: self._producer.send(self._topic, quote),
                num_retries=15,
                exception_type=KafkaTimeoutError,
                error_message='Kafka timed out...',
            )
