from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

def check_client(apikey, secret):
    try:
        client = Client(apikey, secret)
        client.get_account()

        return True, "연결 성공", client

    except BinanceAPIException as e:
        return False, e.message, None

    except BinanceRequestException as e:
        return False, "네트워크 오류: " + str(e),None
    
    except Exception as e:
        return False, "기타 오류:" + str(e),None