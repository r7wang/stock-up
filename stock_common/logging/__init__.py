from .log import logger, Logger

from stock_common import settings
from stock_common.config import ConfigBucket

__all__ = [
    'Logger',
]


def initialize(config_bucket: ConfigBucket) -> None:
    """Subscribes the logger to log level updates

    :param config_bucket: Bucket where log level can be found.
    """

    def _update_log_level():
        level = config_bucket.get_str(settings.CONFIG_KEY_LOG_LEVEL).upper()
        logger.setLevel(level)

    # Permanent subscription; no need to worry about subscription ids.
    config_bucket.subscribe(settings.CONFIG_KEY_LOG_LEVEL, _update_log_level)
