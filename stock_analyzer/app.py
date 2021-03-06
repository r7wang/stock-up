from stock_analyzer.listener_factory import ListenerFactory
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_common import settings, utils
from stock_common.config import ConfigBucket, ConfigListener, LogSubscriber, log_config

if __name__ == "__main__":
    log_config(settings)
    config_bucket = ConfigBucket()
    config_listener = ConfigListener(
        host=settings.CONFIG_HOST,
        base_prefix='stock-analyzer',
        bucket=config_bucket,
    )
    LogSubscriber.initialize(config_bucket)

    with config_listener:
        listener = ListenerFactory.build()
        utils.handle_termination_signal(listener)
        pipeline = StockQuotePipeline()
        listener.start(pipeline.handler)
