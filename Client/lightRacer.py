import pygame
import time
import random

light_speed = 15
window_w = 720
window_h = 480

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption('Light Racer')
game_window = pygame.display.set_mode((window_w, window_h))
fps = pygame.time.Clock()

# Light 1
light_position = [100, 50]
light_body = [[100, 50]]

# Light 2
light_position_2 = [620, 460]
light_body_2 = [[620, 460]]

change_to = direction = 'RIGHT'
change_to_2 = direction_2 = 'LEFT'

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

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_z:
                change_to_2 = 'UP'
            if event.key == pygame.K_s:
                change_to_2 = 'DOWN'
            if event.key == pygame.K_q:
                change_to_2 = 'LEFT'
            if event.key == pygame.K_d:
                change_to_2 = 'RIGHT'

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

    if change_to_2 == 'UP' and direction_2 != 'DOWN':
        direction_2 = 'UP'
    if change_to_2 == 'DOWN' and direction_2 != 'UP':
        direction_2 = 'DOWN'
    if change_to_2 == 'LEFT' and direction_2 != 'RIGHT':
        direction_2 = 'LEFT'    
    if change_to_2 == 'RIGHT' and direction_2 != 'LEFT':
        direction_2  = 'RIGHT'
    
    if direction_2 == 'UP':
        light_position_2[1] -= 10
    if direction_2 == 'DOWN':
        light_position_2[1] += 10
    if direction_2 == 'LEFT':
        light_position_2[0] -= 10
    if direction_2 == 'RIGHT':
        light_position_2[0] += 10

    new_segment = list(light_position)
    light_body.insert(0, new_segment)    

    new_segment_2 = list(light_position_2)
    light_body_2.insert(0, new_segment_2)
    print(new_segment)
    print(new_segment_2)

    game_window.fill(black)

    if (light_position[0] < 0 or light_position[0] > window_w-10 or 
        light_position[1] < 0 or light_position[1] > window_h-10 or
        light_position_2[0] < 0 or light_position_2[0] > window_w-10 or 
        light_position_2[1] < 0 or light_position_2[1] > window_h-10):
        game_over()

    for block in light_body[1:]:
        if pygame.Rect(light_position[0], light_position[1], 10, 10).colliderect(pygame.Rect(block[0], block[1], 10, 10)):
            game_over()

    for block in light_body_2[1:]:
        if pygame.Rect(light_position_2[0], light_position_2[1], 10, 10).colliderect(pygame.Rect(block[0], block[1], 10, 10)):
            game_over()

    for block in light_body:
        if pygame.Rect(light_position_2[0], light_position_2[1], 10, 10).colliderect(pygame.Rect(block[0], block[1], 10, 10)):
            game_over()

    for block in light_body_2:
        if pygame.Rect(light_position[0], light_position[1], 10, 10).colliderect(pygame.Rect(block[0], block[1], 10, 10)):
            game_over()


    for pos in light_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in light_body_2:
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.display.update()

    fps.tick(light_speed)
