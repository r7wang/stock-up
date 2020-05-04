import itertools
from collections import defaultdict
from typing import List

import influxdb

from stock_analyzer.time_util import TimeUtil
from stock_analyzer.time_window import TimeWindow
from stock_common import settings
from stock_common.log import logger
from stock_common.stock_quote import StockQuote


class StockQuotePipeline:
    def __init__(self):
        self._time_windows = defaultdict(lambda: TimeWindow(interval=60000))
        self._time_util = TimeUtil()
        self._db_client = influxdb.InfluxDBClient(
            host=settings.INFLUXDB_HOST,
            port=settings.INFLUXDB_PORT,
            username=settings.INFLUXDB_USER,
            password=settings.INFLUXDB_PASSWORD,
            database=settings.INFLUXDB_DB_NAME,
        )

    def handler(self, quotes: List[StockQuote]) -> None:
        now_timestamp = self._time_util.now()
        for symbol, group in itertools.groupby(quotes, lambda quote: quote.symbol):
            self._time_windows[symbol].update(group, now_timestamp)

        metric_data = self._get_metrics(now_timestamp)
        if not metric_data:
            return

        write_result = self._db_client.write_points(
            points=metric_data,
            time_precision='ms',
            protocol='line',
        )
        if not write_result:
            logger.warn('Could not write to influx')

    def _get_metrics(self, now_timestamp: int) -> List[str]:
        """Get list of metrics in InfluxDB line format

        See link for details:
            https://v2.docs.influxdata.com/v2.0/reference/syntax/line-protocol/

        :param now_timestamp: The timestamp to use for all metrics, in milliseconds.
        :return: List of strings in line format.
        """

        metric_data = []
        for symbol in self._time_windows:
            time_window = self._time_windows[symbol]

            trans_metric = self._format_int_metric(
                'transactions',
                symbol,
                time_window.get_transaction_count(),
                now_timestamp,
            )
            metric_data.append(trans_metric)

            volume_metric = self._format_int_metric(
                'volume',
                symbol,
                time_window.get_volume(),
                now_timestamp,
            )
            metric_data.append(volume_metric)

            min_price = time_window.get_min_price()
            if min_price:
                min_price_metric = self._format_float_metric(
                    'min_price',
                    symbol,
                    float(min_price),
                    now_timestamp,
                )
                metric_data.append(min_price_metric)

            max_price = time_window.get_max_price()
            if max_price:
                max_price_metric = self._format_float_metric(
                    'max_price',
                    symbol,
                    float(max_price),
                    now_timestamp,
                )
                metric_data.append(max_price_metric)

            avg_price_trans = time_window.get_average_price_by_transaction()
            if avg_price_trans:
                avg_price_trans_metric = self._format_float_metric(
                    'avg_price_trans',
                    symbol,
                    float(avg_price_trans),
                    now_timestamp,
                )
                metric_data.append(avg_price_trans_metric)

            avg_price_volume = time_window.get_average_price_by_volume()
            if avg_price_volume:
                avg_price_volume_metric = self._format_float_metric(
                    'avg_price_volume',
                    symbol,
                    float(avg_price_volume),
                    now_timestamp,
                )
                metric_data.append(avg_price_volume_metric)

        return metric_data

    @staticmethod
    def _format_float_metric(name: str, symbol: str, value: float, timestamp: int) -> str:
        return '{name},symbol={symbol} value={value} {timestamp}'.format(
            name=name,
            symbol=symbol,
            value=value,
            timestamp=timestamp,
        )

    @staticmethod
    def _format_int_metric(name: str, symbol: str, value: int, timestamp: int) -> str:
        return '{name},symbol={symbol} value={value}i {timestamp}'.format(
            name=name,
            symbol=symbol,
            value=value,
            timestamp=timestamp,
        )
