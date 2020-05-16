import time
from typing import Any, Callable, Optional, Type

from stock_common.log import logger


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
