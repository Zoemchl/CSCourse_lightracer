import pygame

class Light:
    def __init__(self, position, color, direction, controls):
        self.position = position.copy()
        self.body = [position.copy()]
        self.color = color
        self.change_to = self.direction = direction
        self.controls = controls
        
    def move(self):
        if self.change_to in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            self.direction = self.change_to
        moves = {
            'UP': (0, -10),
            'DOWN': (0, 10),
            'LEFT': (-10, 0),
            'RIGHT': (10, 0)
        }
        move = moves[self.direction]
        self.position[0] += move[0]
        self.position[1] += move[1]
        self.body.insert(0, self.position.copy())

    def handle_input(self, move):
        if move in self.controls.values():
            self.change_to = move

class LightRacerGame:
    def __init__(self):
        self.window_w = 720
        self.window_h = 480
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0),
            'blue': pygame.Color(0, 0, 255)
        }

        controls_1 = {
            'UP': 'UP',
            'DOWN': 'DOWN',
            'LEFT': 'LEFT',
            'RIGHT': 'RIGHT'
        }
        self.light1 = Light([100, 50], self.colors['green'], 'RIGHT', controls_1)

        controls_2 = {
            'UP': 'UP',
            'DOWN': 'DOWN',
            'LEFT': 'LEFT',
            'RIGHT': 'RIGHT'
        }
        self.light2 = Light([620, 460], self.colors['blue'], 'LEFT', controls_2)

    def draw_lights(self, window):
        
        for segment in self.light1.body:
            pygame.draw.rect(window, self.light1.color, pygame.Rect(segment[0], segment[1], 10, 10))

        for segment in self.light2.body:
            pygame.draw.rect(window, self.light2.color, pygame.Rect(segment[0], segment[1], 10, 10))

    def check_collisions(self, light):
        if light.position[0] < 0 or light.position[0] >= self.window_w:
            return True
        if light.position[1] < 0 or light.position[1] >= self.window_h:
            return True

        if light.position in light.body[1:]:
            return True

        return False

    def check_light_collisions(self, light1, light2):
        if light1.position in light2.body:
            return True
        return False

    def update_game(self, light1_move, light2_move):
        self.light1.handle_input(light1_move)
        self.light2.handle_input(light2_move)

        self.light1.move()
        self.light2.move()

        game_over = False

        if (self.check_collisions(self.light1) or 
            self.check_collisions(self.light2) or 
            self.check_light_collisions(self.light1, self.light2) or 
            self.check_light_collisions(self.light2, self.light1)):
            game_over = True

        return {
            'game_over': game_over,
            'light1': self.light1.body,
            'light2': self.light2.body
        }
