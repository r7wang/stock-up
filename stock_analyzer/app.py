from stock_analyzer.kafka_builder import make_stock_quote_consumer
from stock_analyzer.server import Server
from stock_common import settings

if __name__ == "__main__":
    consumer = make_stock_quote_consumer(settings.TOPIC, settings.BROKERS)
    server = Server(consumer)
    server.start()
