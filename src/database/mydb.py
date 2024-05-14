from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, registry


reg = registry()


class Base(DeclarativeBase):
    registry = reg


connection_string = 'mysql://root:password@localhost:3306/trading_ai'
engine = create_engine(connection_string, echo=True)
factory = sessionmaker(bind=engine)
session = factory()

