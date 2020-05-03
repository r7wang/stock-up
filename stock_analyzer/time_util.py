import time


class TimeUtil:
    def now(self) -> int:
        """Fetches the Unix timestamp corresponding to the current time, in milliseconds"""

        return round(time.time() * 1000)
