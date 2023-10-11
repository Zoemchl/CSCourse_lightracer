import pygame
import time

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

    def handle_input(self, key):
        if key in self.controls:
            self.change_to = self.controls[key]

class LightRacerGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Light Racer')

        self.light_speed = 15
        self.window_w = 720
        self.window_h = 480
        self.game_window = pygame.display.set_mode((self.window_w, self.window_h))
        self.fps = pygame.time.Clock()
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0),
            'blue': pygame.Color(0, 0, 255)
        }

        controls_1 = {
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT'
        }
        self.light1 = Light([100, 50], self.colors['green'], 'RIGHT', controls_1)

        controls_2 = {
            pygame.K_z: 'UP',
            pygame.K_s: 'DOWN',
            pygame.K_q: 'LEFT',
            pygame.K_d: 'RIGHT'
        }
        self.light2 = Light([620, 460], self.colors['blue'], 'LEFT', controls_2)

    def game_over(self):
        my_font = pygame.font.SysFont('arial', 50)
        game_over_surface = my_font.render('Game Over Mate :(', True, self.colors['red'])
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_w / 2, self.window_h / 2)
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()

    def check_collisions(self, light):
        if light.position[0] < 0 or light.position[0] > self.window_w-10:
            return True
        if light.position[1] < 0 or light.position[1] > self.window_h-10:
            return True
        for segment in light.body[1:]:
            if segment == light.position:
                return True
        return False

    def check_light_collisions(self, light1, light2):
        if light1.position in light2.body:
            return True
        return False

    def draw_lights(self):
        for pos in self.light1.body:
            pygame.draw.rect(self.game_window, self.light1.color, pygame.Rect(pos[0], pos[1], 10, 10))
        for pos in self.light2.body:
            pygame.draw.rect(self.game_window, self.light2.color, pygame.Rect(pos[0], pos[1], 10, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.light1.handle_input(event.key)
                    self.light2.handle_input(event.key)

            self.light1.move()
            self.light2.move()

            if self.check_collisions(self.light1) or self.check_collisions(self.light2) or self.check_light_collisions(self.light1, self.light2) or self.check_light_collisions(self.light2, self.light1):
                self.game_over()

            self.game_window.fill(self.colors['black'])
            self.draw_lights()
            pygame.display.flip()
            self.fps.tick(self.light_speed)

if __name__ == "__main__":
    game = LightRacerGame()
    game.run()
