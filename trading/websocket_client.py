from binance import ThreadedWebsocketManager

class PriceSocket:
    def __init__(self, symbol, callback):
        self.symbol = symbol
        self.callback = callback
        self.twm = ThreadedWebsocketManager()

    def start(self):
        self.twm.start()
        self.twm.start_symbol_ticker_socket(
            callback=self.handle_message,
            symbol=self.symbol
        )

    def handle_message(self, msg):
        price = float(msg['c']) 
        symbol = msg['s'] 
        self.callback(symbol, price)