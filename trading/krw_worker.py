from PyQt5.QtCore import QThread, pyqtSignal
import requests

class RateWorker(QThread):
    rate_updated = pyqtSignal(float)

    def run(self):
        while True:
            try:
                res = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-USDT", timeout=2)
                rate = res.json()[0]['trade_price']

                self.rate_updated.emit(rate)

            except Exception as e:
                print(e)

            self.sleep(5)