from src.data_providers.providers.data_provider_factory import DataProviderFactory
from src.database.mydb import engine

with engine.connect() as connection:
    data_provider = DataProviderFactory()
    data_provider.get_data_provider()
    data_provider.provider.get_client()
    data_provider.provider.subscribe()
    data_provider.provider.run(runtime=4)
    data_provider.provider.run_server()
    data_provider.provider.close()
