import threading
from server.server import LightRacerServer
from client.client import LightRacerClient

def start_server():
    server = LightRacerServer()
    server.start('127.0.0.1', 65432)

def start_client():
    client = LightRacerClient('127.0.0.1', 65432)
    client.start()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    import time
    time.sleep(2)

    start_client()
