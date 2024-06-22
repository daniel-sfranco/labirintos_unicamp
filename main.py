import pygame
from drawer import draw_init, draw_maze, draw_pause_button, draw_pause_menu, set_screen, draw_HUD
from player import Player
from game_generator import GameGenerator
from save import count_saves, order_saves, save, delete_save
import sys
import os
game_part = 'init'
mouse_x, mouse_y = 0, 0
pressed = False
drawed_maze = False
level = 1
first_unit = 0
width, height = size
change_time = pygame.USEREVENT + 1
time = 60
game: GameGenerator = GameGenerator(1)
player: Player = Player('', 0)
clock = pygame.time.Clock()
while True:
    clock.tick(50)
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
        if event.type == change_time:
            game.time -= 1
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
        if 'last_time' in locals():
            del locals()['last_time']
    elif 'load' in game_part:
        games = return_saves()
        index = int(game_part[4:]) - 1
        game = games[index][1]
        player = games[index][2]
        game_part = 'play'
        unit_size = draw_maze(player, game)
        pygame.display.flip()
        drawed_maze = True
        last_time = game.time
    elif game_part == 'play':
        font = pygame.font.Font('freesansbold.ttf', 32)
        game.time = time - (pygame.time.get_ticks() - game.start - game.dif) // 1000
        if 'last_time' in locals(): game.time -= time - last_time
        if first_unit == 0:
            first_unit = unit_size
            game.start = pygame.time.get_ticks()
        if game.time == 0:
            player.lives -= 1
            game.reset(time)
            player.coordinate = (0, 0)
            game.start = pygame.time.get_ticks()
        if player.lives == 0:
            game_part = 'init'
        player.move_player(game)
        unit_size = draw_maze(player, game)
        pause_rect = draw_pause_button(first_unit)
        game_hud = draw_HUD(lab = level, unit = first_unit)
        pygame.display.flip()
        if pressed and pause_rect.collidepoint(mouse_x, mouse_y):
            game_part = 'pause'
            game.stop = pygame.time.get_ticks()
            pressed = False
        if player.coordinate == (len(game.maze) - 1, len(game.maze[0]) - 1):
            level += 1
            game_part = 'new'
    elif game_part == 'pause':
        game.dif = pygame.time.get_ticks() - game.stop
        pause_menu = draw_pause_menu(player, game)
        pygame.display.flip()
        if pressed:
            if pause_menu[0].collidepoint(mouse_x, mouse_y):
                game_part = 'play'
            elif pause_menu[1].collidepoint(mouse_x, mouse_y):
                player.coordinate = (0, 0)
                game.reset(time)
                game_part = 'play'
            elif pause_menu[2].collidepoint(mouse_x, mouse_y):
                if count_saves() < 3:
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
                        now_saves = count_saves()
                        order_saves(return_saves())
                        game_part = 'pause'
                        pressed = False
                        break
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
    else:
        game_part = 'init'
