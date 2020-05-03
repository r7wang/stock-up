import kafka
from kafka import TopicPartition, OffsetAndMetadata

from stock_common import settings
from stock_common.log import logger


class Server:
    def __init__(self, consumer: kafka.KafkaConsumer):
        self._consumer = consumer
        self._is_done = False

    def start(self) -> None:
        partitions = self._consumer.partitions_for_topic(settings.TOPIC)
        logger.info('Partitions: {}'.format(', '.join(partitions)))

        # Assume that only one partition exists.
        topic_partition = TopicPartition(topic=settings.TOPIC, partition=0)
        begin_offsets = self._consumer.beginning_offsets([topic_partition])
        end_offsets = self._consumer.end_offsets([topic_partition])
        logger.info('Starting offset: {}'.format(begin_offsets[topic_partition]))
        logger.info('Last offset: {}'.format(end_offsets[topic_partition]))

        while not self._is_done:
            result = self._consumer.poll(1000, max_records=50)
            if topic_partition not in result:
                continue

            quotes = []
            last_offset = None
            for message in result[topic_partition]:
                last_offset = max(last_offset, message.offset)
                quotes.append(message.value)
            if last_offset:
                self._commit_offsets(topic_partition, last_offset)

    def stop(self) -> None:
        self._is_done = True

    def _commit_offsets(self, topic_partition: TopicPartition, last_offset: int):
        self._consumer.commit({
            topic_partition: OffsetAndMetadata(offset=last_offset + 1, metadata=''),
        })
