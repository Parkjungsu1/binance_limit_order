import requests


def get_usdt_krw(self):
    try:
        url = "https://api.upbit.com/v1/ticker?markets=KRW-USDT"
        res = requests.get(url)
        data = res.json()

        self.usdt_krw = data[0]['trade_price']
        print("KRW <-> USDT :", self.usdt_krw)

    except Exception as e:
        print("환율 오류:", e)