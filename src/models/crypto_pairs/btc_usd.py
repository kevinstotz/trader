from sqlalchemy import Column, String

from src.database.dataminer_database import Base


class BTC_USD(Base):
    __tablename__ = 'btc_usd'
    timestamp = Column(String(255), primary_key=True)
    low = Column(String(255))
    high = Column(String(255))
    open = Column(String(255))
    close = Column(String(255))
    volume = Column(String(255))

