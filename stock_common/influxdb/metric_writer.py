from typing import List

import influxdb

from stock_common import settings
from stock_common.log import logger


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

    def write(self, metric_data: List[str]) -> None:
        write_result = self._db_client.write_points(
            points=metric_data,
            time_precision='ms',
            protocol='line',
        )
        if not write_result:
            logger.warn('Could not write to influx')
