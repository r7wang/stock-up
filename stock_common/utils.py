import signal
import time
from typing import Any, Callable, Optional, Type

from stock_common.logging import logger


def handle_termination_signal(listener):
    """Handles common signals using a standard approach to ensure that applications terminate gracefully.

    :param listener: Must expose a stop() function.
    """

    def signal_stop(sig_num: int, frame):
        logger.info('Handling signal {}'.format(sig_num))
        if listener:
            logger.info('Stopping listener...')
            listener.stop()

    signal.signal(signal.SIGINT, signal_stop)
    signal.signal(signal.SIGTERM, signal_stop)


def retry(
    func: Callable,
    resolution_func: Optional[Callable],
    num_retries: int,
    exception_type: Type,
    error_message: str,
) -> Any:
    for i in range(num_retries + 1):
        try:
            return func()
        except exception_type:
            logger.info('{} {}'.format(error_message, i))
            if resolution_func:
                resolution_func()
            time.sleep(1)
