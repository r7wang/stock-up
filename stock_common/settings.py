import os

# Where to find the stream of stock quote data.
QUOTE_SERVER = os.environ.get('QUOTE_SERVER')
QUOTE_API_TOKEN = os.environ.get('QUOTE_API_TOKEN')

CONFIG_HOST = os.environ.get('CONFIG_HOST')
CONFIG_KEY_LOG_LEVEL = 'log-level'

MESSAGE_QUEUE_TYPE = os.environ.get('MESSAGE_QUEUE_TYPE')

KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST')
INFLUXDB_PORT = os.environ.get('INFLUXDB_PORT')
INFLUXDB_USER = os.environ.get('INFLUXDB_USER')
INFLUXDB_PASSWORD = os.environ.get('INFLUXDB_PASSWORD')
INFLUXDB_DB_NAME = os.environ.get('INFLUXDB_DB_NAME')
