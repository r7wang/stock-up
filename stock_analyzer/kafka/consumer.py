import pickle
from collections import Callable
from typing import List

import kafka
from kafka import OffsetAndMetadata, TopicPartition
from kafka.errors import NoBrokersAvailable

from stock_analyzer.stock_quote_listener import StockQuoteListener
from stock_common import utils
from stock_common.logging import Logger
from stock_common.stock_quote import StockQuote

CONSUMER_POLL_TIMEOUT_MS = 1000
CONSUMER_POLL_MAX_RECORDS = 50


class KafkaConsumer(StockQuoteListener):

    def __init__(self, brokers: List[str], topic: str):
        self._brokers = brokers
        self._topic = topic
        self._consumer = None
        self._is_done = False
        self._logger = Logger(type(self).__name__)

    def start(self, handler: Callable) -> None:
        """Starts listening for stock quotes if the listener has never been stopped

        :param handler: Callback function invoked for every batch of stock quotes, with the following signature:
            quotes: List[StockQuote]
            return: None
        """
        self._connect()

        partitions = self._consumer.partitions_for_topic(self._topic)
        self._logger.info('partitions: {}'.format(', '.join(map(lambda partition: str(partition), partitions))))

        # Assume that only one partition exists.
        topic_partition = TopicPartition(topic=self._topic, partition=0)
        begin_offsets = self._consumer.beginning_offsets([topic_partition])
        end_offsets = self._consumer.end_offsets([topic_partition])
        last_committed_offset = self._consumer.committed(topic_partition)
        self._logger.info('starting offset: {}'.format(begin_offsets[topic_partition]))
        self._logger.info('last offset: {}'.format(end_offsets[topic_partition]))
        self._logger.info('last committed offset: {}'.format(last_committed_offset))

        while not self._is_done:
            self._process_batch(topic_partition, handler)

        self._logger.info("closing consumer")
        self._consumer.close(autocommit=False)

    def stop(self) -> None:
        self._is_done = True

    def _commit_offsets(self, topic_partition: TopicPartition, offset: int):
        """Commits offsets for the partition of a given topic.

        This effectively advances the index so that future reads from the same Kafka consumer group will not read any
        records up to that offset.

        :param topic_partition: Partition of the topic where offsets are to be committed.
        :param offset: Largest offset read so far.
        :return:
        """

        self._consumer.commit({
            topic_partition: OffsetAndMetadata(offset=offset + 1, metadata=''),
        })

    def _connect(self) -> None:
        self._consumer: kafka.KafkaConsumer = utils.retry(
            lambda: kafka.KafkaConsumer(
                self._topic,
                bootstrap_servers=self._brokers,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                group_id='my-group',
                value_deserializer=lambda item: pickle.loads(item),
            ),
            None,
            num_retries=15,
            exception_type=NoBrokersAvailable,
            error_message='broker unavailable...',
            logger=self._logger,
        )

    def _poll_records(self, topic_partition: TopicPartition) -> (List[StockQuote], int):
        """Polls for records from the partition of a given topic.

        :param topic_partition: Partition of the topic to be polled.
        :return: Tuple of:
            quotes: List of StockQuote objects received from this round of polling. Can be empty.
            max_offset: The largest offset for the objects received. If no objects were received, return 0.
        """
        result = self._consumer.poll(CONSUMER_POLL_TIMEOUT_MS, max_records=CONSUMER_POLL_MAX_RECORDS)
        if topic_partition not in result:
            return [], 0

        quotes = []
        max_offset = 0
        for message in result[topic_partition]:
            max_offset = max(max_offset, message.offset)
            quote: StockQuote = message.value
            quotes.append(quote)
        return quotes, max_offset

    def _process_batch(self, topic_partition: TopicPartition, handler: Callable) -> None:
        quotes, max_offset = self._poll_records(topic_partition)
        if not quotes:
            return

        handler(quotes)
        self._logger.debug('max offset: {}'.format(max_offset))
        self._commit_offsets(topic_partition, max_offset)
