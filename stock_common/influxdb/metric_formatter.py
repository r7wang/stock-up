from decimal import Decimal
from typing import Callable, List, Optional, Union

OptionalNumeric = Optional[Union[Decimal, float, int]]


class MetricFormatter:
    """
    Helper class for formatting metrics in InfluxDB line format. For format details, see the link below.

    https://v2.docs.influxdata.com/v2.0/reference/syntax/line-protocol/
    """

    def __init__(self):
        # While it may seem like we're mapping types to types, what we're actually doing is mapping types to functions
        # that accept an object and return a different type of object.
        self._conversion_map = {
            Decimal: float,
        }

        # Only post-conversion types need to be added to this mapping.
        self._format_map = {
            int: '{name},symbol={symbol} value={value}i {timestamp}',
            float: '{name},symbol={symbol} value={value} {timestamp}',
        }

    def get_formatter(self, symbol: str, timestamp: int) -> Callable[[str, OptionalNumeric], List[str]]:
        """Get callback function that will format metrics in InfluxDB line format

        :param symbol: The stock ticker symbol to use for all metrics.
        :param timestamp: The timestamp to use for all metrics, in milliseconds.
        :return:
        """

        def _format_metric(name: str, value: OptionalNumeric) -> List[str]:
            """Format metric in InfluxDB line format

            :param name: Metric name.
            :param value: Metric value.
            :return: List containing zero or one formatted metric string.
            """

            # Zero values should still be allowed by the formatter.
            if value is None:
                return []

            value_type = type(value)
            if value_type in self._conversion_map:
                value = self._conversion_map[value_type](value)

            value_type = type(value)
            format_str = self._format_map[value_type]
            return [format_str.format(
                name=name,
                symbol=symbol,
                value=value,
                timestamp=timestamp,
            )]

        return _format_metric
