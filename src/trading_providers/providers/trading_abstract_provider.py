from abc import ABC, abstractmethod
from typing import Any


class TradingProviderABC(ABC):

    @abstractmethod
    def create_order(self, order: str, product: str, size: int, leverage: float) -> dict:
        ...

    @abstractmethod
    def get_order(self, order_id: str) -> dict:
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> dict:
        ...
