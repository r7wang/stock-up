from typing import List

from stock_analyzer.time_window import TimeWindow
from stock_common.stock_quote import StockQuote


class StockQuotePipeline:
    def __init__(self, time_window: TimeWindow):
        self._time_window = time_window

    def handler(self, quotes: List[StockQuote]) -> None:
        self._time_window.update(quotes)
