from decimal import Decimal


class StockQuote:
    def __init__(self, timestamp: int, symbol: str, price: Decimal, volume: int):
        self.timestamp = timestamp
        self.symbol = symbol
        self.price = price
        self.volume = volume

    def get_hash(self):
        return self.timestamp, self.symbol, self.price, self.volume
