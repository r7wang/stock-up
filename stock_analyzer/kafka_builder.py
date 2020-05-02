import json
from typing import List

import kafka
from kafka.errors import NoBrokersAvailable

from stock_common import utils


def make_stock_quote_consumer(topic: str, brokers: List[str]) -> kafka.KafkaConsumer:
    return utils.retry(
        lambda: kafka.KafkaConsumer(
            topic,
            bootstrap_servers=brokers,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='my-group',
            value_deserializer=lambda item: json.loads(item.decode('utf-8')),
        ),
        num_retries=15,
        exception_type=NoBrokersAvailable,
        error_message='No brokers available...',
    )
