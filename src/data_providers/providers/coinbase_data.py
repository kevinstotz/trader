from coinbase.websocket import WSClient
import socket
from environs import Env

from src.data_providers.providers.data_abstract_provider import DataProviderABC

env = Env()
env.read_env()


class CoinbaseData(DataProviderABC):
    api_key: str = None
    api_secret: str = None
    client: WSClient = None
    port: int = 0
    host: str = None
    s: socket = None
    data: list = []

    def __init__(self, api_key: str, api_secret: str, port: int = 0, host: str = None):
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        if port == 0:
            self.port = env.int("PORT", 0)
        else:
            self.port = port
        if host is None:
            self.host = env.str("HOST", "Nada")
        else:
            self.host = host

    def get_data(self):
        if len(self.data) > 0:
            return self.data.pop()
        return None

    def set_data(self, msg):
        self.data.append(msg)

    def get_client(self) -> WSClient:
        if self.client is None:
            self.client = WSClient(api_key=self.api_key,
                                   api_secret=self.api_secret,
                                   on_message=self.on_message,
                                   verbose=True)
            self.client.open()
        return self.client

    def subscribe(self, products=None, channels=None):
        if channels is None:
            channels = ["heartbeats", "ticker"]
        if products is None:
            products = ["BTC-USD"]

        self.client.subscribe(products, channels=channels)

    def run(self, runtime: int = 0):
        if runtime == 0:
            self.client.run_forever_with_exception_check()
        else:
            self.client.sleep_with_exception_check(sleep=runtime)

    def run_server(self):
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(0)
        self.s.setblocking(True)
        print(f"Listening on {self.host}:{self.port}")
        connections = []

        try:
            connection, client_address = self.s.accept()
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
            while True:
                buffer = self.get_data()
                if buffer is not None:
                    for connection in connections:
                        connection.send(buffer.encode("utf-8")[:1024])
        except KeyboardInterrupt:
            return
        finally:
            self.s.close()

    def close(self):
        try:
            self.s.close()
        finally:
            self.client.close()

    def on_message(self, msg):
        # print(msg)
        self.set_data(msg)
