import logging

from stock_common.config import ConfigReactor
from stock_common.logging import logger


class LoggingReactor(ConfigReactor):
    """Used to modify the log level when the log level is dynamically changed."""

    def react(self, val: str) -> None:
        """React to log level updates.

        :param val: Log level to use for future logging.
        """

        level = logging.getLevelName(val.upper())
        logger.setLevel(level)
        logger.info('Configuring log level to {}, value={}'.format(val, level))
