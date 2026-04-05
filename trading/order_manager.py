from config.settings import SELL_OFFSET
import time

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

    def _close_position(self, symbol, side, retry=0):
        if retry > 5:
            print(f"❌ {symbol} 청산 실패: 수동 확인 필요")
            return False

        try:
            # 1. 기존 주문 취소 (ReduceOnly 에러 방지)
            self.client.futures_cancel_all_open_orders(symbol=symbol)

            # 2. 거래소 정보에서 해당 코인의 소수점 자릿수(Precision) 가져오기
            exchange_info = self.client.futures_exchange_info()
            symbol_info = next((item for item in exchange_info['symbols'] if item['symbol'] == symbol), None)
            
            if not symbol_info:
                print(f"❌ {symbol} 정보를 찾을 수 없습니다.")
                return False

            # 가격 소수점 자릿수 (pricePrecision) 추출
            price_precision = int(symbol_info['pricePrecision'])

            # 3. 내 실제 포지션 수량 조회
            pos_info = self.client.futures_position_information(symbol=symbol)
            target = next((p for p in pos_info if p['symbol'] == symbol and float(p['positionAmt']) != 0), None)

            if not target:
                print(f"✅ {symbol} 포지션 없음")
                return True

            amt = float(target['positionAmt'])
            quantity = abs(amt)
            actual_side = "SELL" if amt > 0 else "BUY"

            # 4. 현재가 조회 및 규격에 맞는 소수점 처리
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            
            # 중요: 해당 코인의 pricePrecision만큼만 반올림 및 문자열 변환
            str_price = "{: .{}f}".format(current_price, price_precision).strip()

            print(f"🚀 [{symbol}] {str_price} (자릿수: {price_precision}) 지정가 청산 시도")

            # 5. 지정가 주문 제출
            order = self.client.futures_create_order(
                symbol=symbol,
                side=actual_side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=str_price,
                reduceOnly=True
            )

            time.sleep(2)
            status = self.client.futures_get_order(symbol=symbol, orderId=order['orderId'])

            if status['status'] == "FILLED":
                print(f"✅ {symbol} 지정가 청산 완료!")
                return True
            else:
                self.client.futures_cancel_order(symbol=symbol, orderId=order['orderId'])
                # 가격을 현재가로 다시 갱신해서 재시도
                return self._close_position(symbol, actual_side, retry + 1)

        except Exception as e:
            print(f"❌ 즉시 청산 에러 상세: {e}")
            return False