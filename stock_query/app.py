from stock_common import settings, utils
from stock_common.config import ConfigListener
from stock_common.logging import LoggingReactor
from stock_query.producer_factory import ProducerFactory
from stock_query.stock_quote_listener import StockQuoteListener
from stock_query.stock_quote_pipeline import StockQuotePipeline
from stock_query.stock_quote_writer import StockQuoteWriter

if __name__ == "__main__":
    with ConfigListener(
        config_server=settings.CONFIG_SERVER,
        base_prefix='stock-query',
        reactors={
            'log-level': LoggingReactor(),
        },
    ) as config:
        listener = StockQuoteListener(settings.API_TOKEN)
        utils.handle_termination_signal(listener)
        producer = ProducerFactory.build()
        producer.connect()
        writer = StockQuoteWriter(producer)
        pipeline = StockQuotePipeline(writer)

        listener.start(pipeline.handler)

        # Listener is no longer running. Cleanup resources.
        producer.close()
