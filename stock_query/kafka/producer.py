import pickle
from typing import List

import kafka
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

from stock_common import utils
from stock_common.logging import Logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_producer import StockQuoteProducer


class KafkaProducer(StockQuoteProducer):

    def __init__(self, brokers: List[str], topic: str):
        self._brokers = brokers
        self._topic = topic
        self._producer = None
        self._logger = Logger(type(self).__name__)

    def close(self) -> None:
        """Gracefully terminate connection between the producer and the broker."""

        self._logger.info('flushing & closing')
        self._producer.flush()
        self._producer.close()

    def connect(self) -> None:
        """Instantiate connection between the producer and the broker."""

        self._logger.info('connecting to broker')
        self._producer = utils.retry(
            lambda: kafka.KafkaProducer(
                bootstrap_servers=self._brokers,
                value_serializer=lambda item: pickle.dumps(item),
            ),
            None,
            num_retries=15,
            exception_type=NoBrokersAvailable,
            error_message='broker unavailable...',
            logger=self._logger,
        )

    def send(self, quote: StockQuote) -> None:
        """Send a stock quote to the broker."""

        utils.retry(
            lambda: self._producer.send(self._topic, quote),
            None,
            num_retries=15,
            exception_type=KafkaTimeoutError,
            error_message='send timeout...',
            logger=self._logger,
        )
