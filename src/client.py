import socket
from environs import Env

env = Env()
env.read_env()


def run_client(port: int = 0, host: str = None):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == 0:
        server_port = env.int("PORT", 0)
    else:
        server_port = port
    if host is None:
        server_ip = env.str("HOST", "Nada")
    else:
        server_ip = host
    client.connect((server_ip, server_port))

    try:
        while True:
            response = client.recv(1024)
            response = response.decode("utf-8")
            if response.lower() == "closed":
                break
            if len(response) > 0:
                print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")


run_client()
