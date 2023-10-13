import pygame
import socket

from networking import create_socket_client, send_object, receive_object
from lightRacerGame import LightRacerGame

class LightRacerClient:
    def __init__(self, host, port):
        self.client_socket = create_socket_client(host, port)
        print(f"Connected to server at {host}:{port}")
        pygame.init()
        self.game = LightRacerGame()
        self.game_window = pygame.display.set_mode((self.game.window_w, self.game.window_h))


    def start(self):
        print("Starting client loop...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    action = None
                    if event.key in self.game.light1.controls:
                        action = {'player': 1, 'move': self.game.light1.controls[event.key]}

                    if action:
                        print("Sending action to server...")
                        send_object(self.client_socket, action)
                        print("Action sent to server.")

            self.game_window.fill(self.game.colors['black'])
            self.game.draw_lights(self.game_window)
            pygame.display.flip()

            try:
                print("Receiving game data from server...")
                game_data = receive_object(self.client_socket)
                if game_data is None:
                    print("Disconnected from server or received invalid data.")
                    running = False
                    break
                if game_data:
                    print(f"Received game data: {game_data}")
                    self.game.light1.body = game_data.get('light1')
                    self.game.light2.body = game_data.get('light2')
                if game_data.get('message') == 'player_disconnected':
                    print(f"Player {game_data['player_id']} disconnected!")
            except socket.timeout:
                print("Socket timed out. Continuing...")
            except Exception as e:
                print(f"Error receiving game data: {e}")
                running = False

        self.client_socket.close()


if __name__ == "__main__":
    client = LightRacerClient('127.0.0.1', 65432)
    client.start()
