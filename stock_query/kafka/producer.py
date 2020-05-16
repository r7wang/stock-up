import pickle
from typing import List

import kafka
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

from stock_common import utils
from stock_common.log import logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_producer import StockQuoteProducer


class KafkaProducer(StockQuoteProducer):
    def __init__(self, brokers: List[str], topic: str):
        self._topic = topic
        self._producer: kafka.KafkaProducer = self._connect(brokers)

    def close(self):
        logger.info('Flushing Kafka producer...')
        self._producer.flush()
        self._producer.close()

    def send(self, quote: StockQuote):
        utils.retry(
            lambda: self._producer.send(self._topic, quote),
            None,
            num_retries=15,
            exception_type=KafkaTimeoutError,
            error_message='Kafka timed out...',
        )

    def _connect(self, brokers: List[str]):
        logger.info('Connecting to Kafka broker...')
        return utils.retry(
            lambda: kafka.KafkaProducer(
                bootstrap_servers=brokers,
                value_serializer=lambda item: pickle.dumps(item),
            ),
            num_retries=15,
            exception_type=NoBrokersAvailable,
            error_message='Kafka broker unavailable...',
        )