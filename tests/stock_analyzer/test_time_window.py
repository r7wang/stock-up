from decimal import Decimal
from typing import List
from unittest.mock import MagicMock

from stock_analyzer.time_window import TimeWindow
from stock_common.stock_quote import StockQuote


class TestUpdate:
    def _mock_time_util(self, mocker, timestamp: int) -> MagicMock:
        util = MagicMock()
        mocker.patch.object(util, 'now', return_value=timestamp)
        return util

    def _make_quotes(self) -> List[StockQuote]:
        return [
            StockQuote(timestamp=1588368385881, symbol='AMZN', price=Decimal('2279.9'), volume=1),
            StockQuote(timestamp=1588368390816, symbol='AMZN', price=Decimal('2278.74'), volume=10),
            StockQuote(timestamp=1588368391313, symbol='AMZN', price=Decimal('2278.74'), volume=12),
            StockQuote(timestamp=1588368392383, symbol='AMZN', price=Decimal('2279.89'), volume=1),
            StockQuote(timestamp=1588368411117, symbol='AMZN', price=Decimal('2279.89'), volume=6),
        ]

    def test_when_has_expired_quotes(self, mocker):
        service = TimeWindow(1000)
        service._time_util = self._mock_time_util(mocker, 1588368411117)
        service.update(self._make_quotes())

        # Expect expired quotes to be removed.
        expected = Decimal('2279.89')
        assert service.get_average_price_by_transaction() == expected
        assert service.get_average_price_by_volume() == expected
        assert service.get_min_price() == expected
        assert service.get_max_price() == expected
        assert service.get_transaction_count() == 1

    def test_when_window_includes_all_quotes(self, mocker):
        service = TimeWindow(30000)
        service._time_util = self._mock_time_util(mocker, 1588368411117)
        service.update(self._make_quotes())

        # Expect all quotes to be present.
        assert service.get_average_price_by_transaction() == Decimal('2279.432')
        assert service.get_average_price_by_volume() == Decimal('2279.047')
        assert service.get_min_price() == Decimal('2278.74')
        assert service.get_max_price() == Decimal('2279.9')
        assert service.get_transaction_count() == 5

    def test_when_window_includes_no_quotes(self, mocker):
        service = TimeWindow(1000)
        service._time_util = self._mock_time_util(mocker, 1588368450000)
        service.update(self._make_quotes())

        # Expect no quotes.
        assert service.get_average_price_by_transaction() is None
        assert service.get_average_price_by_volume() is None
        assert service.get_min_price() is None
        assert service.get_max_price() is None
        assert service.get_transaction_count() == 0
