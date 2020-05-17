import signal

from stock_analyzer.listener_factory import ListenerFactory
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_common.log import logger

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if listener:
            logger.info("Stopping listener...")
            listener.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    listener = ListenerFactory.build()
    pipeline = StockQuotePipeline()
    listener.start(pipeline.handler)
