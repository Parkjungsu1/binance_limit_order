from config.settings import SELL_OFFSET

class OrderManager:

    def __init__(self, client):
        self.client = client
        self.current_price = 0

    def update_price(self, price):
        self.current_price = price

    def sell(self):
        if self.current_price == 0:
            print("가격 없음")
            return

        sell_price = self.current_price * SELL_OFFSET

        print(f"매도 주문: {sell_price}")

        self.client.create_order(
            symbol=SYMBOL,
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=QUANTITY,
            price=str(sell_price)
        )

    def get_positions(self):
        positions = self.client.futures_position_information()

        result = []
        for p in positions:
            amt = float(p['positionAmt'])
            if amt != 0:
                result.append({
                    "symbol": p['symbol'],
                    "amount": amt,
                    "entryPrice": float(p['entryPrice']),
                    "unRealizedProfit": float(p['unRealizedProfit'])
                })

        return result