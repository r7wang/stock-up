# import requests
# import threading
#
# from stock_query import settings
#
#
# def get_quote():
#     threading.Timer(3.0, get_quote).start()
#     r = requests.get('https://finnhub.io/api/v1/quote?symbol=SHOP&token={}'.format(settings.TOKEN))
#     print(r.json())
#
#
# get_quote()
import signal

from stock_common import settings
from stock_common.log import logger
from stock_query.kafka_builder import make_stock_quote_producer
from stock_query.server import Server
from stock_query.stock_quote_listener import StockQuoteListener
from stock_query.stock_quote_reader import StockQuoteReader
from stock_query.stock_quote_writer import StockQuoteWriter

if __name__ == "__main__":
    def signal_stop(sig_num: int, frame):
        logger.info("Handling signal {}".format(sig_num))
        if server:
            logger.info("Stopping server...")
            server.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)

    producer = make_stock_quote_producer(settings.BROKERS)
    listener = StockQuoteListener(settings.API_TOKEN)
    reader = StockQuoteReader()
    writer = StockQuoteWriter(producer, settings.TOPIC)
    server = Server(listener, reader, writer)
    server.start()

    # Server is no longer running. Cleanup resources.
    logger.info("Flushing Kafka producer...")
    producer.flush()
    producer.close()
