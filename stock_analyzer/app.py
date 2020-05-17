from stock_analyzer.listener_factory import ListenerFactory
from stock_analyzer.stock_quote_pipeline import StockQuotePipeline
from stock_common import utils

if __name__ == "__main__":
    listener = ListenerFactory.build()
    utils.handle_termination_signal(listener)
    pipeline = StockQuotePipeline()
    listener.start(pipeline.handler)
