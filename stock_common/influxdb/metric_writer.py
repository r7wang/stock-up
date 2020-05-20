from typing import List

import influxdb
from influxdb.exceptions import InfluxDBClientError

from stock_common import settings
from stock_common.logging import Logger


class MetricWriter:
    """
    Helper class for writing metrics in InfluxDB line format. For format details, see the link below.

    https://v2.docs.influxdata.com/v2.0/reference/syntax/line-protocol/
    """

    def __init__(self):
        self._db_client = influxdb.InfluxDBClient(
            host=settings.INFLUXDB_HOST,
            port=settings.INFLUXDB_PORT,
            username=settings.INFLUXDB_USER,
            password=settings.INFLUXDB_PASSWORD,
            database=settings.INFLUXDB_DB_NAME,
        )
        self._logger = Logger(type(self).__name__)

    def write(self, metric_data: List[str]) -> None:
        try:
            self._logger.debug('metric data: {}'.format(metric_data))
            write_result = self._db_client.write_points(
                points=metric_data,
                time_precision='ms',
                protocol='line',
            )
            if not write_result:
                self._logger.warning('could not write to influx')
        except InfluxDBClientError as ex:
            if ex.code == 400:
                # We are expecting to catch the following scenarios:
                #   - writing points that are older than the retention policy
                self._logger.warning('write_points client error [code={}, content={}]'.format(ex.code, ex.content))
            else:
                raise
