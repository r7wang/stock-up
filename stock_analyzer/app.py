import signal

from stock_analyzer.kafka_builder import make_stock_quote_consumer
from stock_analyzer.stock_quote_listener import StockQuoteListener
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_analyzer.time_window import TimeWindow
from stock_common import settings
from stock_common.log import logger

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if listener:
            logger.info("Stopping listener...")
            listener.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    consumer = make_stock_quote_consumer(settings.TOPIC, settings.BROKERS)
    listener = StockQuoteListener(consumer)
    time_window = TimeWindow(interval=60000)
    pipeline = StockQuotePipeline(time_window)
    listener.start(pipeline.handler)

    # Listener is no longer running. Cleanup resources.
    logger.info("Closing Kafka consumer...")
    consumer.close(autocommit=False)
