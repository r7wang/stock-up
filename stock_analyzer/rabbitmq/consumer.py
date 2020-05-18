import pickle
from typing import Callable, Optional

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from pika.spec import Basic, BasicProperties

from stock_analyzer.stock_quote_listener import StockQuoteListener
from stock_common import settings, utils
from stock_common.logging import logger
from stock_common.stock_quote import StockQuote


class RmqConsumer(StockQuoteListener):
    def __init__(self):
        self._conn = None
        self._channel: Optional[BlockingChannel] = None
        self._is_done = False

    def start(self, handler: Callable) -> None:
        def _on_message(
                channel: BlockingChannel,
                method: Basic.Deliver,
                properties: BasicProperties,
                body: bytes,
        ) -> None:
            quote: StockQuote = pickle.loads(body)
            handler([quote])
            channel.basic_ack(method.delivery_tag)

        self._connect()
        self._declare_resources()

        self._channel.basic_consume(
            queue=settings.RMQ_QUEUE_QUOTES,
            on_message_callback=_on_message,
            auto_ack=False,
            exclusive=False,
        )
        while not self._is_done:
            self._channel.start_consuming()

        if self._conn and self._conn.is_open:
            logger.info('Closing RabbitMQ connection...')
            self._conn.close()

    def stop(self) -> None:
        self._is_done = True
        self._channel.stop_consuming()

    def _connect(self) -> None:
        if self._conn and not self._conn.is_closed:
            return

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
        self._channel: BlockingChannel = self._conn.channel()

    def _declare_resources(self) -> None:
        """Declare all resources required by the consumer."""

        self._channel.queue_declare(
            queue=settings.RMQ_QUEUE_QUOTES,
            durable=True,
            exclusive=False,
            auto_delete=False,
        )
