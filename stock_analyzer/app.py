from stock_analyzer.listener_factory import ListenerFactory
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_common import settings, utils
from stock_common.config import ConfigBucket, ConfigListener, LogSubscriber

if __name__ == "__main__":
    config_bucket = ConfigBucket()
    config_listener = ConfigListener(
        server=settings.CONFIG_SERVER,
        base_prefix='stock-analyzer',
        bucket=config_bucket,
    )
    LogSubscriber.initialize(config_bucket)

    with config_listener:
        listener = ListenerFactory.build()
        utils.handle_termination_signal(listener)
        pipeline = StockQuotePipeline()
        listener.start(pipeline.handler)
