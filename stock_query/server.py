import json
from collections import deque
from json.decoder import JSONDecodeError

import kafka
import websocket
from kafka.errors import KafkaTimeoutError

from stock_common import utils
from stock_query.stock_quote_parser import StockQuoteParser


class Server:
    def __init__(self, api_token: str, producer: kafka.KafkaProducer, topic: str):
        self.api_token = api_token
        self.stock_quote_parser = StockQuoteParser()
        self.producer = producer
        self.topic = topic
        self.dedup_cache = deque()
        self.dedup_cache_max_size = 10

    def start(self):
        def _on_message(ws, message):
            try:
                data = json.loads(message)
            except JSONDecodeError:
                print('Unknown message: {}'.format(message))
                return

            quotes = self.stock_quote_parser.read(data)
            for quote in quotes:
                quote_hash = quote.get_hash()
                if quote_hash in self.dedup_cache:
                    continue

                if len(self.dedup_cache) > self.dedup_cache_max_size:
                    self.dedup_cache.popleft()
                self.dedup_cache.append(quote_hash)

                print('Key: {}'.format(quote_hash))
                utils.retry(
                    lambda: self.producer.send(self.topic, quote),
                    num_retries=15,
                    exception_type=KafkaTimeoutError,
                    error_message='Kafka timed out...',
                )

        def _on_error(ws, error):
            print(error)

        def _on_close(ws):
            print("### closed ###")
            self.producer.flush()

        def _on_open(ws):
            ws.send('{"type":"subscribe","symbol":"AMZN"}')

        websocket.enableTrace(True)
        app = websocket.WebSocketApp(
            "wss://ws.finnhub.io?token={}".format(self.api_token),
            on_message=_on_message,
            on_error=_on_error,
            on_close=_on_close,
        )
        app.on_open = _on_open
        app.run_forever()

        print('Stopping stock_query...')
