import signal

from stock_common import settings
from stock_common.log import logger
from stock_query.kafka_builder import make_stock_quote_producer
from stock_query.stock_quote_listener import StockQuoteListener
from stock_query.stock_quote_pipeline import StockQuotePipeline
from stock_query.stock_quote_writer import StockQuoteWriter

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if listener:
            logger.info("Stopping listener...")
            listener.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    listener = StockQuoteListener(settings.API_TOKEN)
    producer = make_stock_quote_producer(settings.BROKERS)
    writer = StockQuoteWriter(producer, settings.TOPIC)
    pipeline = StockQuotePipeline(writer)

    listener.start(pipeline.handler)

    # Listener is no longer running. Cleanup resources.
    logger.info("Flushing Kafka producer...")
    producer.flush()
    producer.close()
