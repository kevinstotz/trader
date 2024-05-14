from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin
from src.database.mydb import Base

DATA_PROVIDER_TABLE_NAME = "data_provider"


@dataclass
class DataProvider(Base, SerializerMixin):
    __tablename__ = DATA_PROVIDER_TABLE_NAME

    id: int = Column(Integer(), primary_key=True, unique=True)
    provider: str = Column(String(100), unique=False, default="coinbase")
    priority: int = Column(Integer(), unique=False, default=1)
    is_active: int = Column(Integer(), unique=False, default=1)
    created_date: datetime = Column(DateTime(), default=datetime.utcnow)
