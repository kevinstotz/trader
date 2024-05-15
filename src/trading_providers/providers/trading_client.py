
from src.database.mydb import engine
from src.trading_providers.providers.trading_provider_factory import TradingProviderFactory

with engine.connect() as connection:
    trading_provider = TradingProviderFactory()
    trading_provider.get_trading_provider(provider_id=1, testing=True)
    trading_provider.provider.create_order(order_id="100_1", product="BTC_USD", size=1)

