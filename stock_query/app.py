from stock_common import settings, utils
from stock_common.config import ConfigBucket, ConfigListener, LogSubscriber, log_config
from stock_query.producer_factory import ProducerFactory
from stock_query.stock_quote_listener import StockQuoteListener
from stock_query.stock_quote_pipeline import StockQuotePipeline
from stock_query.stock_quote_writer import StockQuoteWriter
from stock_query.subscription_manager import SubscriptionManager

if __name__ == "__main__":
    log_config(settings)
    config_bucket = ConfigBucket()
    config_listener = ConfigListener(
        host=settings.CONFIG_HOST,
        base_prefix='stock-query',
        bucket=config_bucket,
    )
    LogSubscriber.initialize(config_bucket)

    with config_listener:
        listener = StockQuoteListener(settings.QUOTE_SERVER, settings.QUOTE_API_TOKEN)
        utils.handle_termination_signal(listener)

        subscription_mgr = SubscriptionManager(listener, config_bucket)
        subscription_mgr.start()

        producer = ProducerFactory.build()
        producer.connect()
        writer = StockQuoteWriter(producer)
        pipeline = StockQuotePipeline(writer)

        listener.start(
            open_handler=subscription_mgr.notify_reset,
            message_handler=pipeline.handler,
        )

        subscription_mgr.stop()

        # Listener is no longer running. Cleanup resources.
        producer.close()
