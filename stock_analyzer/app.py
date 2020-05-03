import signal

from stock_analyzer.kafka_builder import make_stock_quote_consumer
from stock_analyzer.server import Server
from stock_common import settings
from stock_common.log import logger

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if server:
            logger.info("Stopping server...")
            server.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    consumer = make_stock_quote_consumer(settings.TOPIC, settings.BROKERS)
    server = Server(consumer)
    server.start()

    # Server is no longer running. Cleanup resources.
    logger.info("Closing Kafka consumer...")
    consumer.close(autocommit=False)
