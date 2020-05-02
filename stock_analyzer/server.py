import kafka
from kafka import TopicPartition, OffsetAndMetadata
from kafka.consumer.fetcher import ConsumerRecord

from stock_common import settings


class Server:
    def __init__(self, consumer: kafka.KafkaConsumer):
        self.consumer = consumer

    def start(self):
        partitions = self.consumer.partitions_for_topic(settings.TOPIC)
        print('Partitions: {}'.format(partitions))
        topic_partition = TopicPartition(topic=settings.TOPIC, partition=0)
        begin_offsets = self.consumer.beginning_offsets([topic_partition])
        end_offsets = self.consumer.end_offsets([topic_partition])
        print('Begin offsets: {}'.format(begin_offsets))
        print('End offsets: {}'.format(end_offsets))
        last_offset = 0
        for _ in range(15):
            message: ConsumerRecord = next(self.consumer)
            print('Message type: {}'.format(type(message)))
            print('Message: {}'.format(message))
            print('Message offset: {}'.format(message.offset))
            last_offset = message.offset
        offset_metadata = OffsetAndMetadata(offset=last_offset + 1, metadata='')
        self.consumer.commit({
            topic_partition: offset_metadata,
        })

        print('Stopping stock_analyzer...')
