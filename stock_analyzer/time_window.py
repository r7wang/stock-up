import heapq
from collections import deque, defaultdict
from decimal import Decimal
from typing import Deque, Dict, Iterator, List, Optional

from stock_common.stock_quote import StockQuote


# TODO: Implement variance calculations.
class TimeWindow:
    def __init__(self, interval: int):
        """
        :param interval: Time interval of the window, in milliseconds.
        """
        self._interval = interval

        # Stores stock quote prices for efficient min/max range.
        self._range_min_heap: List[Decimal] = []
        self._range_max_heap: List[Decimal] = []
        self._range_counter: Dict[Decimal] = defaultdict(int)

        # Stores all stock quotes within time window for efficient maintenance.
        self._quotes: Deque[StockQuote] = deque()
        self._sum_prices_trans: Decimal = Decimal('0')
        self._sum_prices_volume: Decimal = Decimal('0')
        self._count_prices_volume: int = 0

    def get_average_price_by_transaction(self) -> Optional[Decimal]:
        return self._sum_prices_trans / len(self._quotes) if self._quotes else None

    def get_average_price_by_volume(self) -> Optional[Decimal]:
        return self._sum_prices_volume / self._count_prices_volume if self._count_prices_volume else None

    def get_min_price(self) -> Optional[Decimal]:
        return self._range_min_heap[0] if self._range_min_heap else None

    def get_max_price(self) -> Optional[Decimal]:
        return -self._range_max_heap[0] if self._range_max_heap else None

    def get_transaction_count(self) -> int:
        return len(self._quotes)

    def update(self, quotes: Iterator[StockQuote], now_timestamp: int) -> None:
        """
        Update all necessary metadata to allow fast retrieval of metrics for stock quotes within the last time
        interval.

        :param quotes: Quotes to be added to the time window.
        :param now_timestamp: Used as the current timestamp to decide which quotes to exclude from the window.
        """
        min_timestamp = now_timestamp - self._interval

        self._add_new_quotes(quotes)

        # Removing from the heap first would ensure fewer traversals for heap operations, however there's the
        # possibility for the same price to be removed by an older quote and added by a newer quote. This has the
        # potential of either causing redundant counter/heap operations or adding duplicate prices to the heap.
        self._remove_outdated_quotes(min_timestamp)

        # Counter has already been updated. Ensure that range heaps are aligned with the current counter.
        self._realign_range_min_heap()
        self._realign_range_max_heap()

    def _add_new_quotes(self, quotes: Iterator[StockQuote]) -> None:
        for quote in quotes:
            self._quotes.append(quote)

            # Helper counts need to be updated for constant-time metrics calculations.
            self._sum_prices_trans += quote.price
            self._sum_prices_volume += quote.price * quote.volume
            self._count_prices_volume += quote.volume

            # Ensures that range heaps have no duplicate prices.
            if self._range_counter[quote.price] == 0:
                heapq.heappush(self._range_min_heap, quote.price)
                heapq.heappush(self._range_max_heap, -quote.price)

            self._range_counter[quote.price] += 1

    def _remove_outdated_quotes(self, min_timestamp: int) -> None:
        while self._quotes and self._quotes[0].timestamp < min_timestamp:
            quote = self._quotes.popleft()

            # Helper counts need to be updated for constant-time metrics calculations.
            self._sum_prices_trans -= quote.price
            self._sum_prices_volume -= quote.price * quote.volume
            self._count_prices_volume -= quote.volume

            # Ensures that stray prices aren't continuously left within the counter.
            self._range_counter[quote.price] -= 1
            if self._range_counter[quote.price] == 0:
                del self._range_counter[quote.price]

    def _realign_range_min_heap(self) -> None:
        while self._range_min_heap:
            min_price = self._range_min_heap[0]
            if min_price in self._range_counter:
                break
            heapq.heappop(self._range_min_heap)

    def _realign_range_max_heap(self) -> None:
        while self._range_max_heap:
            max_price = -self._range_max_heap[0]
            if max_price in self._range_counter:
                break
            heapq.heappop(self._range_max_heap)
