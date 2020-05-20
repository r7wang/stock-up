import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


class Logger:
    """High-level context-sensitive logger."""

    def __init__(self, name: Optional[str] = None):
        self._name = name

    def critical(self, message: str):
        self._log(logging.CRITICAL, message)

    def debug(self, message: str):
        self._log(logging.DEBUG, message)

    def error(self, message: str):
        self._log(logging.ERROR, message)

    def info(self, message: str):
        self._log(logging.INFO, message)

    def warning(self, message: str):
        self._log(logging.WARNING, message)

    def _log(self, level: int, message: str):
        if self._name:
            logger.log(level, '{}: {}'.format(self._name, message))
        else:
            logger.log(level, message)
