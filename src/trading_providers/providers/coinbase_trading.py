import http.client
import json
from src.trading_providers.providers.trading_abstract_provider import TradingProviderABC


class CoinbaseTrading(TradingProviderABC):
    api_key: str = None
    api_secret: str = None
    client: RESTClient = None
    timeout: int = 0

    def __init__(self, api_key: str, api_secret: str, base_url: str, timeout: int = 5):
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.timeout: int = timeout
        print(api_key)
        print(api_secret)
        self.client = None

    def get_client(self):
        conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'cb-access-key': 'CB-ACCESS-KEY',
            'cb-access-passphrase': 'PASSPHRASE',
            'cb-access-sign': 'ACCESS-SIGN',
            'cb-access-timestamp': 'TIMESTAMP'
        }
        conn.request("GET", "/accounts", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return self.client

    def create_order(self, order_id: str = "1_1", product="BTC-USD", size=0, leverage=1.0) -> dict:
        import http.client
        import json

        conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'cb-access-key': 'KEY',
            'cb-access-passphrase': 'PH',
            'cb-access-sign': 'SIGN',
            'cb-access-timestamp': 'TS'
        }
        conn.request("POST", "/orders", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def get_order(self, order_id: str) -> dict:
        import http.client
        import json

        conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("GET", "/orders/:order_id", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def cancel_order(self, order_id: str) -> dict:
        import http.client
        import json

        conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'cb-access-key': 'key',
            'cb-access-passphrase': 'ph',
            'cb-access-sign': 'sign',
            'cb-access-timestamp': 'ts'
        }
        conn.request("DELETE", "/orders/:order_id", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
