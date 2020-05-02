import time
from typing import Any, Callable, Type


def retry(func: Callable, num_retries: int, exception_type: Type, error_message: str) -> Any:
    for i in range(num_retries + 1):
        try:
            return func()
        except exception_type:
            print('{} {}'.format(error_message, i))
            time.sleep(1)
