import os

# Where to find the stream of stock quote data.
QUOTE_SERVER = 'ws.finnhub.io'
API_TOKEN = 'bqlk517rh5rfdbi8pdig'

CONFIG_HOST = os.environ.get('CONFIG_HOST')
CONFIG_KEY_LOG_LEVEL = 'log-level'

MESSAGE_QUEUE_TYPE = os.environ.get('MESSAGE_QUEUE_TYPE')

KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

RMQ_HOST = 'rabbitmq'
RMQ_VHOST = 'stocks'
RMQ_USER = 'stock-query'
RMQ_PASSWORD = 'rmq-password'
RMQ_EXCHANGE = 'stocks'
RMQ_QUEUE_QUOTES = 'stock-quotes'

INFLUXDB_HOST = 'influxdb'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'influxdb-password'
INFLUXDB_DB_NAME = 'stock'
