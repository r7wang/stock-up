from stock_common.stock_quote import StockQuote


class StockQuoteProducer:
    def close(self) -> None:
        raise NotImplementedError()

    def connect(self) -> None:
        raise NotImplementedError()

    def send(self, quote: StockQuote) -> None:
        raise NotImplementedError()
