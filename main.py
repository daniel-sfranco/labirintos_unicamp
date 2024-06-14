import pygame
from drawer import *
from player import *
from maze_generator import *
import sys

pygame.init()
speed = [1 , 1]
game_part = 'init'
button_positions = []
mouse_x, mouse_y = 0, 0
pressed = False
drawed_maze = False
difficulty = 'easy'
unit_size = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pressed = True
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if game_part == 'init':
        button_positions = draw_init()
        buttons = ['new', 'saved', 'winners', 'info', 'quit']
        if pressed:
            for i in range(len(button_positions)):
                if mouse_x >= button_positions[i][0] and mouse_x <= button_positions[i][1] and mouse_y >= button_positions[i][2] and mouse_y <=  button_positions[i][3]:
                    game_part = buttons[i]
                    break
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            game_part = 'new'
    elif game_part == 'new':
        maze_width = 12
        maze_height = 12
        maze = MazeGenerator(maze_width, maze_height)
        game_part = 'play'
        unit_size = draw_maze(maze)
        pygame.display.flip()
        drawed_maze = True
    elif game_part == 'play':
        cord, new_cord = move_player(maze, unit_size)
        if new_cord != cord:
            draw_maze(maze)
            pygame.display.flip()
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
