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
from stock_common import settings
from stock_query.kafka_builder import make_stock_quote_producer
from stock_query.server import Server


if __name__ == "__main__":
    producer = make_stock_quote_producer(settings.BROKERS)
    server = Server(
        settings.API_TOKEN,
        producer,
        settings.TOPIC,
    )
    server.start()
