import random
import pygame
import sys
import os
import time
import drawer
import save
from constants import *
from player import Player
from game_generator import Game
from math import trunc
from questions import ask_question

game = Game(0)
player = Player('')

while True:
    CLOCK.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_part == 'play':
                    start_pause = time.perf_counter()
                    game_part = 'pause'
                elif game_part == 'pause':
                    game.time_dif -= trunc(time.perf_counter() - start_pause)
                    game_part = 'play'
                if game_part == 'character_sel':
                    game_part = "init"
            if game_part == 'character_sel':
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
                if event.key == pygame.K_LEFT:
                    if skin_sel != 0:
                        skin_sel -= 1
                elif event.key == pygame.K_RIGHT:
                    if skin_sel != 3:
                        skin_sel += 1
                elif event.key == pygame.K_RETURN:
                    player = Player(name = user_input, skin = skin_choice)
                    level = 1
                    game_part = 'new'
                    drawed_maze = True
            elif game_part == 'new':
                game_part = 'init'
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pressed = True
        else:
            mouse_pressed = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if game_part == 'init':
        button_positions = drawer.draw_init()
        buttons = ['new', 'select_save', 'winners', 'info', 'quit']
        if mouse_pressed:
            for i in range(len(button_positions)):
                if button_positions[i].collidepoint(mouse_x, mouse_y):
                    game_part = buttons[i]
                    break
            mouse_pressed = False
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            game_part = 'new'
    elif game_part == 'new':
        if not drawed_maze:
            game_part = "character_sel"
        else:
            game = Game(level)
            game_part = 'play'
            player.coordinate = (0, 0)
            unit_size = drawer.draw_maze(player, game)
            pygame.display.flip()
            drawed_maze = True
            game.time_dif = TIME - game.time
            i = 0
    elif game_part == "character_sel":
        buttons_char, arrows, input_box, skin_choice = drawer.draw_character_sel(user_input, input_active, skin_sel)
        player: Player = Player('')
        if mouse_pressed:
            if buttons_char[0].collidepoint(mouse_x, mouse_y):
                game_part = 'init'
            elif buttons_char[1].collidepoint(mouse_x, mouse_y):
                player = Player(name = user_input, skin = skin_choice)
                level = 1
                game_part = 'new'
                drawed_maze = True
            elif arrows[0].collidepoint(mouse_x, mouse_y):
                if skin_sel != 0:
                    skin_sel -= 1
            elif arrows[1].collidepoint(mouse_x, mouse_y):
                if skin_sel != 3:
                    skin_sel += 1
            elif input_box.collidepoint(mouse_x, mouse_y):
                input_active = True
            else:
                input_active = False
            mouse_pressed = False
            if user_input != "":
                player = Player(name=user_input, skin=skin_choice)
            else:
                player = Player(name='jogador', skin=skin_choice)
            level = 1
    elif 'load' in game_part:
        games = save.save.return_saves()
        index = int(game_part[4:]) - 1
        game = games[index][1]
        player = games[index][2]
        i = 0
        while i < game.level + 6:
            random_x = random.randint(0, len(game.maze[0]) - 1)
            random_y = random.randint(0, len(game.maze) - 1)
            if game.maze[random_y][random_x] == 0:
                game.maze[random_y][random_x] = 'n'
                i += 1
        game_part = 'play'
        unit_size = drawer.draw_maze(player, game)
        pygame.display.flip()
        drawed_maze = True
        start_time = time.perf_counter()
        level = game.level
        game.time_dif = TIME - game.time
        
    elif game_part == 'question':
        if not questioned:
            question = ask_question()
            questioned = True
        answer_buttons, isAnswered = draw_question(question, chosen_answer, player)
        if mouse_pressed:
            if answer_buttons[0].collidepoint(mouse_x, mouse_y):
                chosen_answer = 'a'
            elif answer_buttons[1].collidepoint(mouse_x, mouse_y):
                chosen_answer = 'b'
            elif answer_buttons[2].collidepoint(mouse_x, mouse_y):
                chosen_answer = 'c'
            elif answer_buttons[3].collidepoint(mouse_x, mouse_y):
                chosen_answer = 'd'
        if isAnswered:
            time.sleep(1.5)
            game_part = 'play'
            game.time_dif -= trunc(time.perf_counter() - start_question)
            chosen_answer = ''

    elif game_part == 'play':
        act_time = time.perf_counter()
        game.time = TIME - trunc(act_time - game.start) - game.time_dif
        if game.act_points > 0:
            game.points = game.level * trunc((game.act_points - ((TIME - game.time) / 60) * game.act_points) * 100)
        if 'bomb_start' in locals() and 'bomb_coords' in locals():
            bomb_time = BOMB_TIME - trunc(time.perf_counter() - bomb_start)
            if bomb_time <= 0:
                player = game.detonate(player, bomb_coords)
                key_pressed = False
                del bomb_start, bomb_coords
        if game.time == 0:
            player.lives -= 1
            game.act_points = 0
            if player.lives > 0:
                game.reset()
                player.coordinate = (0, 0)
                continue
        if player.lives == 0:
            game_part = 'game_over'
        end = player.move_player(game)
        for teacher in game.teachers:
            game.maze = teacher.move(player, game)
            if abs(teacher.coordinate[0] - player.coordinate[0]) <= 1 and abs(teacher.coordinate[1] - player.coordinate[1]) <= 1 and not questioned:
                game_part = 'question'
                start_question = time.perf_counter()
            elif abs(teacher.coordinate[0] - player.coordinate[0]) > 1 and abs(teacher.coordinate[1] - player.coordinate[1]) > 1 and questioned:
                questioned = False
        unit_size = draw_maze(player, game)
        pause_rect = draw_pause_button()
        draw_HUD(game, player)
        pygame.display.flip()
        if (mouse_pressed and pause_rect.collidepoint(mouse_x, mouse_y)):
            game_part = 'pause'
            start_pause = time.perf_counter()
            mouse_pressed = False
        if keys[pygame.K_SPACE] and not key_pressed:
            if player.bombs > 0:
                key_pressed = True
                bomb_time = time.perf_counter()
                bomb_start = bomb_time
                player.bombs -= 1
                game.maze[player.coordinate[0]][player.coordinate[1]] += 'ab'
                bomb_coords = player.coordinate
        if end:
            level += 1
            player.points += game.points
            game_part = 'new'
    elif game_part == 'pause':
        pause_menu = drawer.draw_pause_menu(player, game)
        pygame.display.flip()
        if mouse_pressed:
            if pause_menu[0].collidepoint(mouse_x, mouse_y):
                game_part = 'play'
                game.time_dif -= trunc(time.perf_counter() - start_pause)
            elif pause_menu[1].collidepoint(mouse_x, mouse_y):
                player.coordinate = (0, 0)
                player.lives = 3
                game.reset()
                game_part = 'play'
            elif pause_menu[2].collidepoint(mouse_x, mouse_y):
                if save.count_saves(SAVE) < 3:
                    save.save(game, player)
                else:
                    game_part = 'over_save'
            elif pause_menu[3].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                level = 1
                game_part = 'new'
            elif pause_menu[4].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                level = 1
                game_part = 'init'
            mouse_pressed = False
    elif game_part == 'select_save':
        save_menu = drawer.draw_select_save()
        saves = save.return_saves()
        save.order_saves(saves)
        buttons: list[str] = []
        for i in range(1, len(save_menu) - 1):
            buttons.append(f'game {i}')
        buttons.append('clear')
        buttons.append('back')
        if mouse_pressed:
            for i in range(len(save_menu)):
                if save_menu[i].collidepoint(mouse_x, mouse_y):
                    if buttons[i] == 'back':
                        game_part = 'init'
                        mouse_pressed = False
                        break
                    elif buttons[i] == 'clear':
                        if os.path.exists(SAVE):
                            os.remove(SAVE)
                    else:
                        game_part = f'load{buttons[i].replace("game ", "")}'
                        mouse_pressed = False
                        break
    elif game_part == 'over_save':
        save_menu = drawer.draw_select_save('delete', player, game)
        buttons: list[str] = []
        for i in range(1, len(save_menu) - 1):
            buttons.append(f'game {i}')
        buttons.append('clear')
        buttons.append('back')
        if mouse_pressed:
            for i in range(len(save_menu)):
                if save_menu[i].collidepoint(mouse_x, mouse_y):
                    if buttons[i] == 'back':
                        game_part = 'pause'
                        mouse_pressed = False
                        break
                    elif buttons[i] == 'clear':
                        if os.path.exists('save.che'):
                            os.remove('save.che')
                    else:
                        game_number = int(buttons[i].replace('game ', ''))
                        save.delete_save(game_number)
                        save.save(game, player, game_number)
                        now_saves = save.count_saves(SAVE)
                        save.order_saves(save.return_saves())
                        game_part = 'pause'
                        mouse_pressed = False
                        break
    elif game_part == 'game_over':
        over_menu = drawer.draw_game_over(game, player)
        if saved is False:
            save.store_save(game, player)
            saved = True
        pygame.display.flip()
        if mouse_pressed:
            if over_menu[0].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                saved = False
                game_part = 'new'
            elif over_menu[1].collidepoint(mouse_x, mouse_y):
                print(":)")
            elif over_menu[2].collidepoint(mouse_x, mouse_y):
                drawed_maze = False
                saved = False
                game_part = 'init'
            mouse_pressed = False
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
    else:
        game_part = 'init'
