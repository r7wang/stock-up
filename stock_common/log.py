import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


class LoggingReactor:
    def react(self, val: str):
        level = logging.getLevelName(val.upper())
        logger.setLevel(level)
        logger.info('Set log level to {}'.format(level))
