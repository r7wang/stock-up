import logging

from stock_common.config import ConfigReactor
from stock_common.logging import logger, Logger


class LoggingReactor(ConfigReactor):
    """Used to modify the log level when the log level is dynamically changed."""

    def __init__(self):
        self._logger = Logger(type(self).__name__)

    def react(self, val: str) -> None:
        """React to log level updates.

        :param val: Log level to use for future logging.
        """

        level_str = val.upper()
        level = logging.getLevelName(level_str)
        logger.setLevel(level)
        self._logger.info('setting log level to {}'.format(level_str))
