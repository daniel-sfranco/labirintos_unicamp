import pygame
from constants import *
from drawer import *
from player import Player
from game_generator import GameGenerator
from save import count_saves, order_saves, save, delete_save, store_save
import sys
import os
import time
from math import trunc

game_part = 'init'
mouse_x, mouse_y = 0, 0
pressed = False
drawed_maze = False
level = 1
game: GameGenerator = GameGenerator(1)
player: Player = Player('', 0)
while True:
    CLOCK.tick(50)
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
        player = Player('test-player', 0)
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
        game = GameGenerator(level, 0)
        game_part = 'play'
        player.coordinate = (0, 0)
        unit_size = draw_maze(player, game)
        pygame.display.flip()
        drawed_maze = True
    elif 'load' in game_part:
        games = return_saves()
        index = int(game_part[4:]) - 1
        game = games[index][1]
        player = games[index][2]
        game_part = 'play'
        unit_size = draw_maze(player, game)
        pygame.display.flip()
        drawed_maze = True
        start_time = time.perf_counter()
        def_time = game.time
        level = game.level
    elif game_part == 'play':
        game.time = TIME - trunc(time.perf_counter() - game.start)
        if 'bomb_start' in locals() and 'bomb_coords' in locals():
            bomb_time = BOMB_TIME - trunc(time.perf_counter() - bomb_start)
            if bomb_time <= 0:
                for i in range(bomb_coords[0]-1, bomb_coords[0]+2):
                    for j in range(bomb_coords[1]-1, bomb_coords[1]+2):
                        if i >= 0 and i < len(game.maze) and j >= 0 and j < len(game.maze[i]):
                            if isinstance(game.maze[i][j], str) and 'p' in game.maze[i][j]:
                                player.lives -= 1
                                player.coordinate = (0, 0)
                                game.reset()
                            game.maze[i][j] = 0
                del bomb_start, bomb_coords, bomb_time
        if game.time == 0:
            player.lives -= 1
            if player.lives > 0:
                game.reset()
                player.coordinate = (0, 0)
        if player.lives == 0:
            store_save(game, player)
            game_part = 'init'
        next = player.move_player(game)
        unit_size = draw_maze(player, game)
        pause_rect = draw_pause_button()
        draw_HUD(game, player)
        pygame.display.flip()
        if pressed and pause_rect.collidepoint(mouse_x, mouse_y):
            game_part = 'pause'
            start_pause = time.perf_counter()
            pressed = False
        if keys[pygame.K_SPACE]:
            if player.bombs > 0:
                bomb_time = time.perf_counter()
                bomb_start = bomb_time
                player.bombs -= 1
                game.maze[player.coordinate[0]][player.coordinate[1]] += 'b'
                bomb_coords = player.coordinate
        if player.coordinate == (len(game.maze) - 1, len(game.maze[0]) - 1):
            level += 1
            game_part = 'new'
    elif game_part == 'pause':
        pause_menu = draw_pause_menu(player, game)
        pygame.display.flip()
        if pressed:
            if pause_menu[0].collidepoint(mouse_x, mouse_y):
                game_part = 'play'
                game.default += trunc(time.perf_counter() - start_pause)
            elif pause_menu[1].collidepoint(mouse_x, mouse_y):
                player.coordinate = (0, 0)
                game.reset()
                game_part = 'play'
            elif pause_menu[2].collidepoint(mouse_x, mouse_y):
                if count_saves(SAVE) < 3:
                    save(game, player)
                else:
                    game_part = 'over_save'
            elif pause_menu[3].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                game_part = 'new'
            elif pause_menu[4].collidepoint(mouse_x, mouse_y):
                screen.fill('black')
                drawed_maze = False
                game_part = 'init'
            pressed = False
    elif game_part == 'select_save':
        save_menu = draw_select_save()
        saves = return_saves()
        order_saves(saves)
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
                        if os.path.exists('save.che'):
                            os.remove('save.che')
                    else:
                        game_part = f'load{buttons[i].replace('game ', '')}'
                        pressed = False
                        break
    elif game_part == 'over_save':
        save_menu = draw_select_save('delete', player, game)
        buttons: list[str] = []
        for i in range(1, len(save_menu) - 1):
            buttons.append(f'game {i}')
        buttons.append('clear')
        buttons.append('back')
        if pressed:
            for i in range(len(save_menu)):
                if save_menu[i].collidepoint(mouse_x, mouse_y):
                    if buttons[i] == 'back':
                        game_part = 'pause'
                        pressed = False
                        break
                    elif buttons[i] == 'clear':
                        if os.path.exists('save.che'): os.remove('save.che')
                    else:
                        game_number = int(buttons[i].replace('game ', ''))
                        delete_save(game_number)
                        save(game=game, player=player, game_number=game_number)
                        now_saves = count_saves(SAVE)
                        order_saves(return_saves())
                        game_part = 'pause'
                        pressed = False
                        break
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
    else:
        game_part = 'init'
