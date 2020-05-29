from stock_common import settings
from stock_query.kafka import KafkaProducer
from stock_query.rabbitmq import RmqProducer
from stock_query.stock_quote_producer import StockQuoteProducer


class ProducerFactory:

    @staticmethod
    def build() -> StockQuoteProducer:
        service_map = {
            'kafka': lambda: KafkaProducer(settings.KAFKA_BROKERS.split(','), settings.KAFKA_TOPIC),
            'rmq': lambda: RmqProducer(),
        }
        return service_map[settings.MESSAGE_QUEUE_TYPE]()
