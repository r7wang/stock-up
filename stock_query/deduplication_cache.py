from collections import deque

from stock_common.stock_quote import StockQuote


class DeduplicationCache:
    def __init__(self, max_size: int = 10):
        self._dedup_cache = deque()
        self._dedup_cache_max_size = max_size

    def is_duplicate(self, quote: StockQuote) -> bool:
        quote_hash = quote.get_hash()
        if quote_hash in self._dedup_cache:
            return True

        if len(self._dedup_cache) > self._dedup_cache_max_size:
            self._dedup_cache.popleft()
        self._dedup_cache.append(quote_hash)
        return False
