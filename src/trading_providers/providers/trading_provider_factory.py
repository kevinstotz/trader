from dataclasses import dataclass
from enum import Enum
from typing import Any
from src.database.mydb import session
from src.models.trading_providers.coinbase import CoinbaseTradingModel, COINBASE_TRADING_TABLE_NAME
from src.models.trading_providers.trading_provider import TradingProvider
from src.trading_providers.providers.coinbase_trading import CoinbaseTrading


@dataclass
class TradingProviderListDataMixin:
    table: str
    id: int
    row: int


class TradingProviderList(TradingProviderListDataMixin, Enum):
    COINBASE = COINBASE_TRADING_TABLE_NAME, 1, 1


class TradingProviderFactory:
    provider_model: Any = None
    provider: Any = None
    client: Any = None

    def get_trading_provider(self, provider_id=TradingProviderList.COINBASE.id, testing=True) -> None:

        if provider_id == 0:
            self.provider = session.query(TradingProvider).filter(TradingProvider.is_active == 1).order_by(
                TradingProvider.priority).first()
        else:
            self.provider = session.query(TradingProvider).get(provider_id)

        if self.provider.id == TradingProviderList.COINBASE.id:
            self.provider_model: CoinbaseTradingModel = session.query(CoinbaseTradingModel).get(TradingProviderList.COINBASE.id)
            if testing:
                print("COINBASE TESTING")
                print(self.provider_model.testing_base_url)
                self.provider = CoinbaseTrading(api_key=self.provider_model.testing_api_key,
                                                api_secret=self.provider_model.testing_api_secret,
                                                base_url=self.provider_model.testing_base_url)
            else:
                print("COINBASE LIVE")
                self.provider = CoinbaseTrading(self.provider_model.api_key, self.provider_model.api_secret)
            self.client = self.provider.get_client()
        else:
            print("cant get data provider")
            exit()

        session.close()
