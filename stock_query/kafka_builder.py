import pickle
from typing import List

import kafka
from kafka.errors import NoBrokersAvailable

from stock_common import utils


def make_stock_quote_producer(brokers: List[str]) -> kafka.KafkaProducer:
    return utils.retry(
        lambda: kafka.KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda item: pickle.dumps(item),
        ),
        num_retries=15,
        exception_type=NoBrokersAvailable,
        error_message='No brokers available...',
    )
