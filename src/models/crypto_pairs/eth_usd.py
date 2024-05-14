from sqlalchemy import Column, String

from src.database.mydb import Base


class ETH_USD(Base):
    __tablename__ = 'eth_usd'
    timestamp = Column(String(255), primary_key=True)
    low = Column(String(255))
    high = Column(String(255))
    open = Column(String(255))
    close = Column(String(255))
    volume = Column(String(255))

