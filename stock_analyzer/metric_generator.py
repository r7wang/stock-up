from decimal import Decimal
from typing import List, Optional, Union

from stock_analyzer.time_window import TimeWindow
from stock_common.influxdb import MetricFormatter
from stock_common.log import logger

OptionalNumeric = Optional[Union[Decimal, float, int]]


class MetricGenerator:
    """Generates metrics needed by the stock analyzer"""

    def __init__(self):
        self._metric_formatter = MetricFormatter()

    def get_metrics(self, time_window: TimeWindow, symbol: str, timestamp: int) -> List[str]:
        """Get list of formatted metrics

        :param time_window: Object containing accumulated statistics for a given time window.
        :param symbol: The stock ticker symbol.
        :param timestamp: The timestamp to use for all metrics, in milliseconds.
        :return: List of formatted metrics.
        """

        format_metric = self._metric_formatter.get_formatter(symbol, timestamp)
        try:
            return [
                *format_metric('transactions', time_window.get_transaction_count()),
                *format_metric('volume', time_window.get_volume()),
                *format_metric('last_price', time_window.get_last_price()),
                *format_metric('min_price', time_window.get_min_price()),
                *format_metric('max_price', time_window.get_max_price()),
                *format_metric('avg_price_trans', time_window.get_average_price_by_transaction()),
                *format_metric('avg_price_volume', time_window.get_average_price_by_volume()),
            ]
        except KeyError as ex:
            logger.error('Could not format unsupported metric type: {}'.format(ex))
            return []
