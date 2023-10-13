import socket
import time


import threading
from networking import create_socket_server, send_object, receive_object
from lightRacerGame import LightRacerGame

class LightRacerServer:
    def __init__(self):
        self.clients = []
        self.game = LightRacerGame()
        self.client_counter = 0

    def start(self, host, port):
        self.server_socket = create_socket_server(host, port)
        print(f"Server started. Listening on {host}:{port}...")
        print("Waiting for clients...")
        while len(self.clients) < 2:
            try:
                client_socket, addr = self.server_socket.accept()
                self.client_counter += 1
                print(f"Client {addr} connected as Player {self.client_counter}.")
                self.clients.append((self.client_counter, client_socket))
                print(f"Total connected clients: {len(self.clients)}")
                threading.Thread(target=self.handle_client, args=(client_socket, self.client_counter)).start()
            except socket.timeout:
                print("Socket timed out waiting for a new client. Retrying...")
                continue


    def handle_client(self, client_socket, client_id):
        while True:
            self.send_updates_to_all_clients()
            time.sleep(0.05)
            try:
                data = receive_object(client_socket, timeout=1.0)
                print(f"Received data from Player {client_id}: {data}")
                if not data:
                    print(f"Didn't receive data from Player {client_id} for 1 second.")
                    self.clients = [client for client in self.clients if client[1] != client_socket]
                    client_socket.close()
                    return

                if client_id == 1:
                    self.game.light1.handle_input(data.get('move'))
                    self.game.light1.move()
                elif client_id == 2:
                    self.game.light2.handle_input(data.get('move'))
                    self.game.light2.move()

                game_data = {
                    'light1': self.game.light1.body,
                    'light2': self.game.light2.body
                }

                for _, c in self.clients:
                    send_object(c, game_data)
                    print(f"Sent data to client: {game_data}")

            except socket.timeout:
                print(f"Socket timed out for Player {client_id}. Continuing...")

            except Exception as e:
                print(f"Error with Player {client_id}: {e}")
                self.clients = [client for client in self.clients if client[1] != client_socket]
                client_socket.close()
                
                for _, c in self.clients:
                    send_object(c, {'message': 'player_disconnected', 'player_id': client_id})

    def send_updates_to_all_clients(self):
        game_data = {
            'light1': self.game.light1.body,
            'light2': self.game.light2.body
        }



if __name__ == "__main__":
    server = LightRacerServer()
    server.start('127.0.0.1', 65432)
