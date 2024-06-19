import pygame
from drawer import *
from player import Player
from maze_generator import MazeGenerator
from save import count_saves, save
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

game_part = 'init'
mouse_x, mouse_y = 0, 0
pressed = False
drawed_maze = False
level = 1
first_unit = 0
width, height = size
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_part == 'play':
                    game_part = 'pause'
                else:
                    game_part = 'play'
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pressed = True
        else:
            pressed = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if game_part == 'init':
        button_positions = draw_init()
        buttons = ['new', 'select_save', 'winners', 'info', 'quit']
        if pressed:
            for i in range(len(button_positions)):
                if button_positions[i].collidepoint(mouse_x, mouse_y):
                    game_part = buttons[i]
                    break
            pressed = False
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            game_part = 'new'
    elif game_part == 'new':
        if not drawed_maze:
            level = 1
        maze = MazeGenerator(level, 0)
        player = Player('test_player', 0)
        game_part = 'play'
        unit_size = draw_maze(player, maze)
        pygame.display.flip()
        drawed_maze = True
    elif 'load' in game_part:
        games = return_saves()
        index = int(game_part[4:]) - 1
        maze = games[index][1]
        player = games[index][2]
        game_part = 'play'
        unit_size = draw_maze(player, maze, True)
        pygame.display.flip()
        drawed_maze = True
    elif game_part == 'play':
        if first_unit == 0:
            first_unit = unit_size
        player.move_player(maze)
        unit_size = draw_maze(player, maze)
        pause_rect = draw_pause_button(first_unit)
        pygame.display.flip()
        if pressed and pause_rect.collidepoint(mouse_x, mouse_y):
            game_part = 'pause'
            pressed = False
        if player.coordinate == (len(maze.maze) - 1, len(maze.maze[0]) - 1):
            level += 1
            game_part = 'new'
    elif game_part == 'pause':
        pause_menu = draw_pause_menu()
        pygame.display.flip()
        if pressed:
            if pause_menu[0].collidepoint(mouse_x, mouse_y):
                game_part = 'play'
            elif pause_menu[1].collidepoint(mouse_x, mouse_y):
                player.coordinate = (0, 0)
                maze.reset()
                game_part = 'play'
            elif pause_menu[2].collidepoint(mouse_x, mouse_y):
                save(maze, player)
            elif pause_menu[3].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                game_part = 'new'
            elif pause_menu[4].collidepoint(mouse_x, mouse_y):
                screen.fill('black')
                game_part = 'init'
            pressed = False
    elif game_part == 'select_save':
        save_menu = draw_select_save()
        buttons: list[str] = []
        for i in range(1, len(save_menu) - 1):
            buttons.append(f'game {i}')
        buttons.append('clear')
        buttons.append('back')
        if pressed:
            for i in range(len(save_menu)):
                if save_menu[i].collidepoint(mouse_x, mouse_y):
                    if buttons[i] == 'back':
                        game_part = 'init'
                        pressed = False
                        break
                    elif buttons[i] == 'clear':
                        if os.path.exists('save.che'): os.remove('save.che')
                    else:
                        game_part = f'load{buttons[i].replace('game ', '')}'
                        pressed = False
                        break
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
