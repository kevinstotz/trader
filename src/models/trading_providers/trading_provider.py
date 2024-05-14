from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin
from src.database.mydb import Base

TRADING_PROVIDER_TABLE_NAME = "trading_provider"


@dataclass
class TradingProvider(Base, SerializerMixin):
    __tablename__ = TRADING_PROVIDER_TABLE_NAME

    id: int = Column(Integer(), primary_key=True, unique=True)
    provider: str = Column(String(100), unique=False, default="coinbase")
    priority: int = Column(Integer(), unique=False, default=1)
    is_active: int = Column(Integer(), unique=False, default=1)
    created_date: datetime = Column(DateTime(), default=datetime.utcnow)
