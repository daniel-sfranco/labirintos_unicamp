import random
import pygame
import sys
import os
import time
import drawer
import save
import audio
from manage import Manager
from constants import *
from player import Player
from game_generator import Game
from math import trunc
from questions import Question
from student import get_history

def handle_keydown_event(event: pygame.event.Event, manager: Manager):
    manager.key_pressed = True
    if event.key == pygame.K_ESCAPE:
        if manager.part == 'play':
            manager.start_pause_time = time.perf_counter()
            manager.part = 'pause'
        elif manager.part == 'pause':
            game.time_dif += trunc(time.perf_counter() - manager.start_pause_time)
            manager.part = 'play'
        elif manager.part == 'character_sel':
            manager.part = "init"
        elif manager.part == 'init':
            manager.part = 'quit'
    if manager.part == 'character_sel':
        if manager.input_active:
            if event.key == pygame.K_BACKSPACE:
                manager.user_input = manager.user_input[:-1]
            else:
                manager.user_input += event.unicode
        if event.key == pygame.K_LEFT:
            if manager.skin_sel != 0:
                manager.skin_sel -= 1
                audio.choice.play()
        elif event.key == pygame.K_RIGHT:
            if manager.skin_sel != len(CHARACTERS) - 1:
                manager.skin_sel += 1
                audio.choice.play()
    elif manager.part == 'question':
        alt1 = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]
        alt2 = ['a', 'b', 'c', 'd']
        if event.key in alt1:
            manager.chosen_answer = alt2[alt1.index(event.key)]
    elif manager.part == 'new':
        manager.part = 'init'
    return manager


def init(manager) -> Manager:
    button_positions = drawer.draw_init()
    buttons = ['character_sel', 'select_save', 'winners', 'info', 'quit']
    keys = pygame.key.get_pressed()
    if manager.mouse_pressed:
        for i in range(len(button_positions)):
            if button_positions[i].collidepoint(manager.mouse_x, manager.mouse_y):
                manager.part = buttons[i]
                if buttons[i] != 'quit':
                    audio.select.play()
                break
        manager.mouse_pressed = False
    if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
        manager.part = 'character_sel'
        manager.key_pressed = False
    return manager


def new(game):
    game = Game(game.level + 1)
    player.coordinate = (0, 0)
    drawer.draw_maze(player, game, manager)
    pygame.display.flip()
    game.time_dif = TIME - game.time
    return game


def character_sel(manager: Manager, player: Player) -> tuple[Manager, Player]:
    buttons_char, arrows, input_box, skin_choice = drawer.draw_character_sel(manager)
    if manager.mouse_pressed:
        if buttons_char[0].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
            audio.select.play()
        elif buttons_char[1].collidepoint(manager.mouse_x, manager.mouse_y):
            player = Player(name=manager.user_input, skin=skin_choice)
            manager.part = 'new'
            audio.select.play()
        elif arrows[0].collidepoint(manager.mouse_x, manager.mouse_y):
            if manager.skin_sel != 0:
                manager.skin_sel -= 1
                audio.choice.play()
        elif arrows[1].collidepoint(manager.mouse_x, manager.mouse_y):
            if manager.skin_sel != len(CHARACTERS) - 1:
                manager.skin_sel += 1
                audio.choice.play()
        elif input_box.collidepoint(manager.mouse_x, manager.mouse_y):
            manager.input_active = True
        else:
            manager.input_active = False
        manager.mouse_pressed = False
        if manager.user_input != "":
            player = Player(name=manager.user_input, skin=skin_choice)
        else:
            history = get_history(game)
            player = Player(name=f'Jogador {len(history)}', skin=skin_choice)
    elif manager.key_pressed:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            manager.part = 'new'
            audio.select.play()
            manager.key_pressed = False
            if manager.user_input != "":
                player = Player(name=manager.user_input, skin=skin_choice)
            else:
                history = get_history(game)
                player = Player(name=f'Jogador {len(history)}', skin=skin_choice)
    return manager, player


def load() -> tuple[Game, Player]:
    games = save.return_saves()
    index = int(manager.part[4:]) - 1
    game = games[index][1]
    player = games[index][2]
    i = 0
    drawer.draw_maze(player, game, manager)
    pygame.display.flip()
    game.time_dif = game.time- TIME
    return game, player


def question(manager, game) -> tuple[Manager, Game]:
    if not manager.questioned:
        manager.questioned = True
        manager.chosen_answer = ''
        manager.num_question = random.randint(1, 100)
        return manager, game
    manager.question = Question(manager.num_question)
    manager.question_type = game.maze[manager.question_giver[0]][manager.question_giver[1]]
    answer_buttons, answered = drawer.draw_question(manager, game)
    if manager.mouse_pressed:
        alt = ['a', 'b', 'c', 'd']
        for i in range(4):
            if answer_buttons[i].collidepoint(manager.mouse_x, manager.mouse_y):
                manager.chosen_answer = alt[i]
    if answered is not False:
        if answered == 'right':
            if manager.question_type == 's':
                for student in game.students:
                    if student.coordinate == manager.question_giver:
                        game.maze[manager.question_giver[0]][manager.question_giver[1]] = student.item
                        game.num_students -= 1
                        del game.students[game.students.index(student)]
                        break
            elif manager.question_type == 't':
                for teacher in game.teachers:
                    if teacher.coordinate == manager.question_giver:
                        game.maze[manager.question_giver[0]][manager.question_giver[1]] = 'n'
                        game.num_teachers -= 1
                        del game.teachers[game.teachers.index(teacher)]
                        break
        else:
            if manager.question_type == 's':
                for student in game.students:
                    if student.coordinate == manager.question_giver:
                        game.num_students -= 1
                        del game.students[game.students.index(student)]
                        break
            elif manager.question_type == 't':
                for teacher in game.teachers:
                    if teacher.coordinate == manager.question_giver:
                        game.num_teachers -= 1
                        del game.teachers[game.teachers.index(teacher)]
                        break
            game.maze[manager.question_giver[0]][manager.question_giver[1]] = 0
        pygame.time.delay(1500)
        manager.part = 'play'
        manager.questioned = False
        game.time_dif += trunc(time.perf_counter() - manager.start_question)
        manager.chosen_answer = ''
    return manager, game


def play(manager: Manager, player: Player, game: Game) -> tuple[Manager, Player, Game]:
    manager.question_giver = (-1, -1)
    passed = trunc(time.perf_counter() - game.start) - game.time_dif - player.time_dif
    game.time = TIME - passed
    if game.act_points > 0:
        game.points = round(game.level * game.act_points * (1 - (passed / TIME)) * 100)
    if game.bomb_start != 0 and game.bomb_coords != (-1, -1):
        game.bomb_time = BOMB_TIME - trunc(time.perf_counter() - game.bomb_start)
        if game.bomb_time <= 0:
            player = game.detonate(player, game.bomb_coords)
            manager.key_pressed = False
            game.bomb_start = 0
            game.bomb_coords = (-1, -1)
    if game.time == 0:
        player.lives -= 1
        game.act_points = 0
        if player.lives > 0:
            game.reset()
            player.time_dif = 0
            player.points = player.first_points
            player.coordinate = (0, 0)
            return manager, player, game
    if player.lives == 0:
        manager.part = 'game_over'
    coord = player.coordinate
    next_coordinate = player.move_player(game)
    move = coord == next_coordinate
    for student in game.students:
        if student.coordinate[0] == next_coordinate[0] and student.coordinate[1] == next_coordinate[1]:
            manager.part = 'question'
            manager.question_giver = student.coordinate
            manager.start_question = time.perf_counter()
            return manager, player, game
    for teacher in game.teachers:
        game.maze = teacher.move(player, game, move)
        if abs(teacher.coordinate[0] - player.coordinate[0]) <= 1 and abs(teacher.coordinate[1] - player.coordinate[1]) <= 1:
            manager.part = 'question'
            manager.question_giver = teacher.coordinate
            manager.start_question = time.perf_counter()
        elif teacher.coordinate[0] == next_coordinate[0] and teacher.coordinate[1] == next_coordinate[1]:
            manager.part = 'question'
            manager.question_giver = teacher.coordinate
            manager.start_question = time.perf_counter()
    drawer.draw_maze(player, game, manager)
    pause_rect = drawer.draw_pause_button()
    drawer.draw_HUD(player, game)
    pygame.display.flip()
    if (manager.mouse_pressed and pause_rect.collidepoint(manager.mouse_x, manager.mouse_y)):
        manager.part = 'pause'
        manager.start_pause_time = time.perf_counter()
        manager.mouse_pressed = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not manager.key_pressed:
        if player.bombs > 0:
            manager.key_pressed = True
            game.bomb_time = time.perf_counter()
            game.bomb_start = game.bomb_time
            player.bombs -= 1
            game.maze[player.coordinate[0]][player.coordinate[1]] += 'ab'
            game.bomb_coords = player.coordinate
    if next_coordinate == (-1, -1):
        player.points += game.points
        player.time_dif = 0
        player.first_points = player.points
        manager.part = 'new'
        audio.level_complete.play()
    return manager, player, game


def pause(manager: Manager, player: Player, game: Game) -> tuple[Manager, Player, Game]:
    pause_menu = drawer.draw_pause_menu(player, game, manager)
    pygame.display.flip()
    if manager.mouse_pressed:
        if pause_menu[0].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'play'
            game.time_dif += trunc(time.perf_counter() - manager.start_pause_time)
            audio.select.play()
        elif pause_menu[1].collidepoint(manager.mouse_x, manager.mouse_y):
            player.coordinate = (0, 0)
            player.lives = 3
            player.time_dif = 0
            player.lives = player.first_lives
            player.bombs = player.first_bomb
            player.points = player.first_points
            game.reset()
            manager.part = 'play'
            audio.select.play()
        elif pause_menu[2].collidepoint(manager.mouse_x, manager.mouse_y):
            if save.count_saves(SAVE) < 3:
                save.save(game, player)
            else:
                manager.part = 'over_save'
            audio.select.play()
        elif pause_menu[3].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'new'
            audio.select.play()
        elif pause_menu[4].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
            audio.select.play()
        manager.mouse_pressed = False
    return manager, player, game


def select_save(manager: Manager) -> Manager:
    save_menu = drawer.draw_select_save()
    saves = save.return_saves()
    save.order_saves(saves)
    buttons: list[str] = []
    for i in range(1, len(save_menu) - 1):
        buttons.append(f'game {i}')
    buttons.append('clear')
    buttons.append('back')
    if manager.mouse_pressed:
        for i in range(len(save_menu)):
            if save_menu[i].collidepoint(manager.mouse_x, manager.mouse_y):
                if buttons[i] == 'back':
                    manager.part = 'init'
                    manager.mouse_pressed = False
                    break
                elif buttons[i] == 'clear':
                    if os.path.exists(SAVE):
                        os.remove(SAVE)
                else:
                    manager.part = f'load{buttons[i].replace("game ", "")}'
                    manager.mouse_pressed = False
                    break
    return manager


def over_save(manager: Manager) -> Manager:
    save_menu = drawer.draw_select_save('delete', player, game)
    buttons: list[str] = []
    for i in range(1, len(save_menu) - 1):
        buttons.append(f'game {i}')
    buttons.append('clear')
    buttons.append('back')
    if manager.mouse_pressed:
        for i in range(len(save_menu)):
            if save_menu[i].collidepoint(manager.mouse_x, manager.mouse_y):
                if buttons[i] == 'back':
                    manager.part = 'pause'
                    manager.mouse_pressed = False
                    break
                elif buttons[i] == 'clear':
                    if os.path.exists('save.che'):
                        os.remove('save.che')
                else:
                    game_number = int(buttons[i].replace('game ', ''))
                    save.delete_save(game_number)
                    save.save(game, player, game_number)
                    save.order_saves(save.return_saves())
                    manager.part = 'pause'
                    manager.mouse_pressed = False
                    break
    return manager


def game_over(manager: Manager) -> Manager:
    over_menu = drawer.draw_game_over(game, player, manager)
    pygame.display.flip()
    saves = get_history()
    saved = False
    for save in saves:
        if save[0].startswith(player.name):
            saved = True
    if not saved:
        save.store_save(game, player)
    if manager.mouse_pressed:
        if over_menu[0].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'new'
        elif over_menu[1].collidepoint(manager.mouse_x, manager.mouse_y):
            print(":)")
        elif over_menu[2].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
        manager.mouse_pressed = False
    return manager

def main():
    global game, player, manager
    while manager.running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.running = False
            if event.type == pygame.KEYDOWN:
                manager = handle_keydown_event(event, manager)
            else:
                manager.key_pressed = False
            if pygame.mouse.get_pressed()[0]:
                manager.mouse_x, manager.mouse_y = pygame.mouse.get_pos()
                manager.mouse_pressed = True
            else:
                manager.mouse_pressed = False
        if manager.part == 'init':
            manager = init(manager)
        elif manager.part == 'new':
            game = new(game)
            manager.part = 'play'
        elif manager.part == "character_sel":
            manager, player = character_sel(manager, player)
        elif 'load' in manager.part:
            game, player = load()
            manager.part = 'play'
        elif manager.part == 'question':
            manager, game = question(manager, game)
        elif manager.part == 'winners':
            manager = winners(manager, game)
        elif manager.part == 'info':
            manager = info(manager)
        elif manager.part == 'play':
            play(manager, player, game)
        elif manager.part == 'pause':
            manager, player, game = pause(manager, player, game)
        elif manager.part == 'select_save':
            manager = select_save(manager)
        elif manager.part == 'over_save':
            manager = over_save(manager)
        elif manager.part == 'game_over':
            manager = game_over(manager)
        elif manager.part == 'quit':
            manager.running = False
        else:
            manager.part = 'init'

def winners(manager: Manager, game: Game) -> Manager:
    back_button = drawer.draw_winners(game)
    if manager.mouse_pressed:
        if back_button.collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
            audio.select.play()
    return manager

def info(manager: Manager):
    back_button = drawer.draw_info()
    if manager.mouse_pressed:
        if back_button.collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
            audio.select.play()
    return manager

game: Game = Game(0)
player: Player = Player('')
manager: Manager = Manager()
main()
pygame.quit()
sys.exit()