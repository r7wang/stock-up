import pickle
from typing import Optional

import pika
from pika.channel import Channel
from pika.exceptions import AMQPConnectionError, ConnectionClosed

from stock_common import settings, utils
from stock_common.log import logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_producer import StockQuoteProducer


class RmqProducer(StockQuoteProducer):
    DURABLE_MESSAGE = 2

    def __init__(self):
        self._conn = None
        self._channel: Optional[Channel] = None
        self._default_message_props = pika.BasicProperties(delivery_mode=self.DURABLE_MESSAGE)

    def close(self):
        if self._conn and self._conn.is_open:
            logger.info('Closing RabbitMQ connection...')
            self._conn.close()

    def send(self, quote: StockQuote):
        self._connect()
        utils.retry(
            lambda: self._publish(quote),
            lambda: self._connect(),
            num_retries=15,
            exception_type=ConnectionClosed,
            error_message='RabbitMQ connection not open...',
        )

    def _connect(self) -> None:
        if not self._conn or self._conn.is_closed:
            logger.info('Connecting to RabbitMQ...')
            credentials = pika.PlainCredentials(settings.RMQ_USER, settings.RMQ_PASSWORD)
            params = pika.ConnectionParameters(
                host=settings.RMQ_HOST,
                virtual_host=settings.RMQ_VHOST,
                credentials=credentials,
            )
            self._conn = utils.retry(
                lambda: pika.BlockingConnection(params),
                None,
                num_retries=15,
                exception_type=AMQPConnectionError,
                error_message='RabbitMQ broker unavailable...',
            )
            self._channel: Channel = self._conn.channel()
            self._channel.exchange_declare(
                exchange=settings.RMQ_EXCHANGE,
                exchange_type='direct',
                durable=True,
                auto_delete=False,
                internal=False,
            )
            self._channel.queue_declare(
                queue=settings.RMQ_QUEUE_QUOTES,
                durable=True,
                exclusive=False,
                auto_delete=False,
            )
            self._channel.queue_bind(
                queue=settings.RMQ_QUEUE_QUOTES,
                exchange=settings.RMQ_EXCHANGE,
            )

    def _publish(self, quote: StockQuote) -> None:
        self._channel.basic_publish(
            exchange=settings.RMQ_EXCHANGE,
            routing_key=settings.RMQ_QUEUE_QUOTES,
            body=pickle.dumps(quote),
            properties=self._default_message_props,
            mandatory=False,
        )
