from coinbase.rest import RESTClient
from src.trading_providers.providers.trading_abstract_provider import TradingProviderABC


class CoinbaseTrading(TradingProviderABC):
    api_key: str = None
    api_secret: str = None
    client: RESTClient = None
    timeout: int = 0

    def __init__(self, api_key: str, api_secret: str, timeout: int = 5):
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.timeout: int = timeout
        self.client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=timeout)

    def create_order(self, order: str = "1_1", product="BTC-USD", size=0, leverage=1.0) -> dict:
        order = self.client.market_order(client_order_id=order,
                                         product_id=product,
                                         side="BUY",
                                         leverage=leverage,
                                         quote_size=size)
        return order

    def get_order(self, order_id: str) -> dict:
        order = self.client.get_order(order_id)
        return order

    def cancel_order(self, order_id: str) -> dict:
        order = self.client.cancel_orders([order_id])
        return order
