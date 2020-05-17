import signal

from stock_analyzer.kafka import KafkaConsumer
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_common import settings
from stock_common.log import logger

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if consumer:
            logger.info("Stopping listener...")
            consumer.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    consumer = KafkaConsumer(settings.TOPIC, settings.BROKERS)
    pipeline = StockQuotePipeline()
    consumer.start(pipeline.handler)
