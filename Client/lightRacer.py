import pygame
import time
import random

light_speed = 15

window_w = 720
window_h = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('Light Racer')
game_window = pygame.display.set_mode((window_w, window_h))

fps = pygame.time.Clock()

light_position = [100, 50]
light_body = [
    [100, 50],
]


direction = 'RIGHT'
change_to = direction

# Game over function 

def game_over():

    my_font = pygame.font.SysFont('arial', 50)
    game_over_surface = my_font.render('Game Over Mate :(', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_w/2, window_h/2)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)

    pygame.quit()

    quit()

# Light control 

while True: 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'


    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'    
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction  = 'RIGHT'        


    if direction == 'UP':
        light_position[1] -= 10
    if direction == 'DOWN':
        light_position[1] += 10
    if direction == 'LEFT':
        light_position[0] -= 10
    if direction == 'RIGHT':
        light_position[0] += 10

    new_segment = list(light_position)
    light_body.insert(0, new_segment)    

    game_window.fill(black)

    for pos in light_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

            
# Conditions to loose 

    if light_position[0] < 0 or light_position[0] > window_w-10:
        game_over()
    if light_position[1] < 0 or light_position[1] > window_h-10:
        game_over()

    for block in light_body[1:]:
        if light_position[0] == block[0] and light_position[1] == block[1]:
            game_over()

    pygame.display.update()

    fps.tick(light_speed)