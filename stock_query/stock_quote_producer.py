from stock_common.stock_quote import StockQuote


class StockQuoteProducer:
    def close(self):
        raise NotImplementedError()

    def send(self, quote: StockQuote):
        raise NotImplementedError()
