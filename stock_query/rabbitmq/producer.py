import pickle
from collections import deque
from typing import Deque, Dict, Optional

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError, ConnectionClosed, NackError

from stock_common import settings, utils
from stock_common.logging import Logger
from stock_common.stock_quote import StockQuote
from stock_query.stock_quote_producer import StockQuoteProducer


class RmqProducer(StockQuoteProducer):
    PERSISTENT_MESSAGE = 2

    def __init__(self):
        self._conn = None
        self._channel: Optional[BlockingChannel] = None
        self._default_message_props = pika.BasicProperties(delivery_mode=self.PERSISTENT_MESSAGE)
        self._logger = Logger(type(self).__name__)

        # Storing pending and nacked deliveries in non-persistent storage does pose a risk that the service might be
        # restarted with items in both containers. Losing these items may cause permanent data loss, but we expect the
        # risk to be minimized because:
        #   - pending_deliveries should only contain elements within the last few seconds
        #   - nacked_deliveries should almost always be empty while messages are being sent continuously
        self._pending_deliveries: Dict[int, StockQuote] = {}
        self._nacked_deliveries: Deque[StockQuote] = deque()

        self._acked = 0
        self._nacked = 0
        self._message_number = 0

    def close(self) -> None:
        """Gracefully terminate connection between the producer and the broker."""

        if self._conn and self._conn.is_open:
            self._logger.info('closing connection')
            self._conn.close()

    def connect(self) -> None:
        """Instantiate connection between the producer and the broker, declaring all necessary resources."""

        self._connect()
        self._declare_resources()

    def send(self, quote: StockQuote) -> None:
        """Send a stock quote to the broker.

        Attempt to redeliver all previous undeliverable messages before the current quote.
        """

        while self._nacked_deliveries:
            to_publish = self._nacked_deliveries.popleft()
            self._publish_with_retry(to_publish)
        self._publish_with_retry(quote)

    def _connect(self) -> None:
        """Defines the minimal set of functionality for reconnecting to the broker."""

        if self._conn and not self._conn.is_closed:
            return

        self._logger.info('connecting')
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
            error_message='broker unavailable...',
            logger=self._logger,
        )
        self._channel: BlockingChannel = self._conn.channel()
        self._channel.confirm_delivery()
        self._reset_confirmation_tracking()

    def _declare_resources(self) -> None:
        """Declare all resources required by the producer."""

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

    # def _on_delivery_confirmation(self, method_frame: Method) -> None:
    #     """
    #     Invoked by pika when RabbitMQ responds to a Basic.Publish RPC command, passing in either a Basic.Ack or
    #     Basic.Nack frame with the delivery tag of the message that was published. The delivery tag is an integer
    #     counter indicating the message number that was sent on the channel via Basic.Publish. Here we're just doing
    #     house keeping to keep track of stats and remove message numbers that we expect a delivery confirmation of from
    #     the list used to keep track of messages that are pending confirmation.
    #
    #     :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame.
    #     """
    #
    #     confirmation_type = method_frame.method.NAME.split('.')[1].lower()
    #     delivery_tag = method_frame.method.delivery_tag
    #     logger.info('Thread (delivery confirmation): {}'.format(threading.get_ident()))
    #     logger.info('Received {} for delivery tag: {}'.format(confirmation_type, delivery_tag))
    #     if confirmation_type == 'ack':
    #         self._acked += 1
    #     elif confirmation_type == 'nack':
    #         self._nacked += 1
    #         self._nacked_deliveries.append(self._pending_deliveries[delivery_tag])
    #     del self._pending_deliveries[delivery_tag]
    #     logger.info(
    #         'Published {} messages, {} have yet to be confirmed, {} were acked and {} were nacked'.format(
    #             self._message_number,
    #             len(self._pending_deliveries),
    #             self._acked,
    #             self._nacked,
    #         ),
    #     )

    def _publish(self, quote: StockQuote) -> None:
        utils.retry(
            lambda: self._channel.basic_publish(
                exchange=settings.RMQ_EXCHANGE,
                routing_key=settings.RMQ_QUEUE_QUOTES,
                body=pickle.dumps(quote),
                properties=self._default_message_props,
                mandatory=False,
            ),
            None,
            num_retries=15,
            exception_type=NackError,
            error_message='nacked the published message...',
            logger=self._logger,
        )
        self._message_number += 1
        # self._pending_deliveries[self._message_number] = quote

    def _publish_with_retry(self, quote: StockQuote) -> None:
        utils.retry(
            lambda: self._publish(quote),
            lambda: self._connect(),
            num_retries=15,
            exception_type=ConnectionClosed,
            error_message='connection not open...',
            logger=self._logger,
        )

    def _reset_confirmation_tracking(self) -> None:
        # TODO: What happens to pending deliveries and nacked deliveries? For at least once delivery, assume the
        #       messages all need to be resent.
        self._nacked_deliveries.extend(self._pending_deliveries.values())
        self._pending_deliveries = {}
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
