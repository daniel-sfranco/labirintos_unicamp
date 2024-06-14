import pygame
from drawer import *
from player import *
from maze_generator import *
import sys

pygame.init()
game_part = 'init'
mouse_x, mouse_y = 0, 0
pressed = False
drawed_maze = False
difficulty = 'easy'
maze = []
player = 0
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
        maze_width = 15
        maze_height = 15
        maze = MazeGenerator(maze_width, maze_height)
        player = Player()
        game_part = 'play'
        unit_size = draw_maze(player, maze)
        pygame.display.flip()
        drawed_maze = True
    elif game_part == 'play':
        player.move_player(maze)
        draw_maze(player, maze)
        pygame.display.flip()
        if player.coordinate == (len(maze.maze) - 1, len(maze.maze[0]) - 1):
            game_part = 'quit'
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
