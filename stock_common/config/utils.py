from stock_common import settings
from stock_common.logging import Logger


def log_config(module) -> None:
    logger = Logger('Config')
    attrs = filter(lambda attr: attr[0].isupper(), dir(module))
    for key in attrs:
        val = getattr(settings, key)
        logger.info('{} = {}'.format(key, val))
