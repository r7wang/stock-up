from stock_analyzer.kafka import KafkaConsumer
from stock_analyzer.rabbitmq import RmqConsumer
from stock_analyzer.stock_quote_listener import StockQuoteListener
from stock_common import settings


class ListenerFactory:
    @staticmethod
    def build() -> StockQuoteListener:
        service_map = {
            'kafka': lambda: KafkaConsumer(settings.BROKERS, settings.TOPIC),
            'rmq': lambda: RmqConsumer(),
        }
        return service_map[settings.MESSAGE_QUEUE_TYPE]()
