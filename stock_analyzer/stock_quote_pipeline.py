import itertools
from collections import defaultdict
from typing import List

from stock_analyzer.metric_generator import MetricGenerator
from stock_analyzer.time_util import TimeUtil
from stock_analyzer.time_window import TimeWindow
from stock_common.influxdb import MetricWriter
from stock_common.stock_quote import StockQuote


class StockQuotePipeline:
    def __init__(self):
        self._metric_gen = MetricGenerator()
        self._metric_writer = MetricWriter()
        self._time_windows = defaultdict(lambda: TimeWindow(interval=60000))
        self._time_util = TimeUtil()

    def handler(self, quotes: List[StockQuote]) -> None:
        now_timestamp = self._time_util.now()
        for symbol, group in itertools.groupby(quotes, lambda quote: quote.symbol):
            self._time_windows[symbol].update(group, now_timestamp)

        metric_data = self._get_metrics(now_timestamp)
        if not metric_data:
            return

        self._metric_writer.write(metric_data)

    def _get_metrics(self, timestamp: int) -> List[str]:
        """Get list of formatted metrics for all known stock ticker symbols

        :param timestamp: The timestamp to use for all metrics, in milliseconds.
        :return: List of formatted metrics.
        """

        metric_data = []
        for symbol in self._time_windows:
            time_window = self._time_windows[symbol]
            metric_data.extend(self._metric_gen.get_metrics(time_window, symbol, timestamp))

        return metric_data
