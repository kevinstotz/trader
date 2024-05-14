from src.data_providers.static.static_data_provider_factory import StaticDataProviderFactory
from src.database.mydb import engine

with engine.connect() as connection:
    data_provider = StaticDataProviderFactory()
    data_provider.get_static_data_provider(provider_id=5)
    print(data_provider.client.get_data())
    print(data_provider.client.data.head())
    print(data_provider.client.get_price())
