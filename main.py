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

def handle_keydown_event(event: pygame.event.Event, manager: Manager) -> Manager:
    """
    Process keydown events in a Pygame application, updating the state of the Manager object based on the current game part
    and the specific key pressed.

    Args:
        event (pygame.event.Event): A Pygame event object representing a keydown event.
        manager (Manager): An instance of the Manager class that holds the current state of the game.

    Returns:
        Manager: The updated manager object with the new state based on the key pressed and the current game part.
    """
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


def init() -> Manager:
    # Draw initial menu and get button positions
    button_positions = drawer.draw_init()

    # Define menu options
    buttons = ['character_sel', 'select_save', 'winners', 'info', 'quit']

    # Check mouse click
    if manager.mouse_pressed:
        for i, pos in enumerate(button_positions):
            if pos.collidepoint(manager.mouse_x, manager.mouse_y):
                manager.part = buttons[i]
                if buttons[i] != 'quit':
                    audio.select.play()
                break
        manager.mouse_pressed = False

    # Check key press for Enter key
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
        manager.part = 'character_sel'
        manager.key_pressed = False

    return manager


def new(game: Game) -> Game:
    """
    Initializes a new game level, resets the player's position, redraws the maze, updates the display, and adjusts the game's time difference.

    Args:
        game (Game): An instance of the Game class representing the current game state.

    Returns:
        Game: The newly created Game instance with the updated level and time difference.
    """
    new_game = Game(game.level + 1)
    player.coordinate = (0, 0)
    drawer.draw_maze(player, new_game, manager)
    pygame.display.flip()
    new_game.time_dif = TIME - new_game.time
    return new_game


def character_sel(manager: Manager, player: Player) -> tuple[Manager, Player]:
    """
    Handles the character selection process in the game.

    Args:
    - manager: An instance of the Manager class that tracks the game's state and user inputs.
    - player: An instance of the Player class representing the current player.

    Returns:
    - Updated manager object with the new game state.
    - Updated player object with the selected character and name.
    """
    buttons_char, arrows, input_box, skin_choice = drawer.draw_character_sel(manager)

    if manager.mouse_pressed:
        mouse_x, mouse_y = manager.mouse_x, manager.mouse_y

        if buttons_char[0].collidepoint(mouse_x, mouse_y):
            manager.part = 'init'
            audio.select.play()
        elif buttons_char[1].collidepoint(mouse_x, mouse_y):
            player = Player(name=manager.user_input, skin=skin_choice)
            manager.part = 'new'
            audio.select.play()
        elif arrows[0].collidepoint(mouse_x, mouse_y) and manager.skin_sel != 0:
            manager.skin_sel -= 1
            audio.choice.play()
        elif arrows[1].collidepoint(mouse_x, mouse_y) and manager.skin_sel != len(CHARACTERS) - 1:
            manager.skin_sel += 1
            audio.choice.play()
        elif input_box.collidepoint(mouse_x, mouse_y):
            manager.input_active = True
        else:
            manager.input_active = False

        manager.mouse_pressed = False

        if manager.user_input != "":
            player = Player(name=manager.user_input, skin=skin_choice)
        else:
            history = get_history()
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
                history = get_history()
                player = Player(name=f'Jogador {len(history)}', skin=skin_choice)

    return manager, player


def load() -> tuple[Game, Player]:
    """
    Retrieves a saved game and player state from a list of saved games,
    draws the maze on the screen, updates the game's time difference, and returns the game and player objects.
    """
    games = save.return_saves()
    index = int(manager.part[4:]) - 1
    game, player = games[index][1], games[index][2]
    drawer.draw_maze(player, game, manager)
    pygame.display.flip()

    game.time_dif = game.time - TIME

    return game, player


def question(game: Game, manager: Manager) -> tuple[Game, Manager]:
    """
    Handles presenting a question to the player, capturing their answer, and updating the game state based on correctness.

    Args:
        game (Game): An instance of the Game class representing the current game state.
        manager (Manager): An instance of the Manager class managing the game state and player interactions.

    Returns:
        tuple[Game, Manager]: Updated Game and Manager instances.
    """
    if not manager.questioned:
        manager.questioned = True
        manager.chosen_answer = ''
        manager.num_question = random.randint(1, 100)
        return game, manager

    manager.question = Question(manager.num_question)
    manager.question_type = game.maze[manager.question_giver[0]][manager.question_giver[1]]
    answer_buttons, answered = drawer.draw_question(manager, game)

    if manager.mouse_pressed:
        alt = ['a', 'b', 'c', 'd']
        for i, button in enumerate(answer_buttons):
            if button.collidepoint(manager.mouse_x, manager.mouse_y):
                manager.chosen_answer = alt[i]

    if answered is not False:
        if answered == 'right':
            if manager.question_type == 's':
                for student in game.students:
                    if student.coordinate == manager.question_giver:
                        game.maze[manager.question_giver[0]][manager.question_giver[1]] = student.item
                        game.num_students -= 1
                        game.students.remove(student)
                        break
            elif manager.question_type == 't':
                for teacher in game.teachers:
                    if teacher.coordinate == manager.question_giver:
                        game.maze[manager.question_giver[0]][manager.question_giver[1]] = 'n'
                        game.num_teachers -= 1
                        game.teachers.remove(teacher)
                        break
        else:
            if manager.question_type == 's':
                for student in game.students:
                    if student.coordinate == manager.question_giver:
                        game.num_students -= 1
                        game.students.remove(student)
                        break
            elif manager.question_type == 't':
                for teacher in game.teachers:
                    if teacher.coordinate == manager.question_giver:
                        game.num_teachers -= 1
                        game.teachers.remove(teacher)
                        break
            game.maze[manager.question_giver[0]][manager.question_giver[1]] = 0

        manager.part = 'play'
        manager.questioned = False
        game.time_dif += trunc(time.perf_counter() - manager.start_question)
        manager.chosen_answer = ''
        pygame.time.delay(1500)

    return game, manager


def play(manager: Manager, player: Player) -> tuple[Game, Manager, Player]:
    # Calculate time passed and update game time and points
    passed = trunc(time.perf_counter() - game.start) - game.time_dif - player.time_dif
    game.time = TIME - passed
    if game.act_points > 0:
        game.points = round(game.level * game.act_points * (1 - (passed / TIME)) * 100)

    # Handle bomb detonation
    if game.bomb_start != 0 and game.bomb_coords != (-1, -1):
        game.bomb_time = BOMB_TIME - trunc(time.perf_counter() - game.bomb_start)
        if game.bomb_time <= 0:
            player = game.detonate(player, game.bomb_coords)
            manager.key_pressed = False
            game.bomb_start = 0
            game.bomb_coords = (-1, -1)

    # Check player lives and game over conditions
    if game.time == 0:
        player.lives -= 1
        game.act_points = 0
        if player.lives > 0:
            game.reset()
            player.time_dif = 0
            player.points = player.first_points
            player.coordinate = (0, 0)
            return game, manager, player
    if player.lives == 0:
        manager.part = 'game_over'

    # Handle player movement and interactions with students and teachers
    manager.question_giver = (-1, -1)
    coord = player.coordinate
    next_coordinate = player.move_player(game)
    move = coord == next_coordinate

    for student in game.students:
        if student.coordinate == next_coordinate:
            manager.part = 'question'
            manager.question_giver = student.coordinate
            manager.start_question = time.perf_counter()
            return game, manager, player

    for teacher in game.teachers:
        game.maze = teacher.move(player, game, move)
        if abs(teacher.coordinate[0] - player.coordinate[0]) <= 1 and abs(teacher.coordinate[1] - player.coordinate[1]) <= 1:
            manager.part = 'question'
            manager.question_giver = teacher.coordinate
            manager.start_question = time.perf_counter()
        elif teacher.coordinate == next_coordinate:
            manager.part = 'question'
            manager.question_giver = teacher.coordinate
            manager.start_question = time.perf_counter()

    # Draw game elements
    drawer.draw_maze(player, game, manager)
    pause_rect = drawer.draw_pause_button()
    drawer.draw_HUD(player, game)
    pygame.display.flip()

    # Check for pause button input
    if manager.mouse_pressed and pause_rect.collidepoint(manager.mouse_x, manager.mouse_y):
        manager.part = 'pause'
        manager.start_pause_time = time.perf_counter()
        manager.mouse_pressed = False

    # Check for bomb placement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not manager.key_pressed:
        if player.bombs > 0:
            manager.key_pressed = True
            game.bomb_time = time.perf_counter()
            game.bomb_start = game.bomb_time
            player.bombs -= 1
            game.maze[player.coordinate[0]][player.coordinate[1]] += 'ab'
            game.bomb_coords = player.coordinate

    # Check for level completion
    if next_coordinate == (-1, -1):
        player.points += game.points
        player.time_dif = 0
        player.first_points = player.points
        manager.part = 'new'
        audio.level_complete.play()

    return game, manager, player


def pause(game: Game, manager: Manager, player: Player) -> tuple[Game, Manager, Player]:
    """
    Handles the game's pause menu interactions.

    Draws the pause menu, checks for mouse clicks on menu options, and updates the game state accordingly.

    Args:
        game (Game): An instance of the Game class representing the current game state.
        manager (Manager): An instance of the Manager class managing the game state and user inputs.
        player (Player): An instance of the Player class representing the current player.

    Returns:
        tuple[Game, Manager, Player]: Updated instances of game, manager, and player.
    """
    pause_menu = drawer.draw_pause_menu(player, game, manager)
    pygame.display.flip()

    if manager.mouse_pressed:
        mouse_x, mouse_y = manager.mouse_x, manager.mouse_y

        if pause_menu[0].collidepoint(mouse_x, mouse_y):
            manager.part = 'play'
            game.time_dif += trunc(time.perf_counter() - manager.start_pause_time)
            audio.select.play()

        elif pause_menu[1].collidepoint(mouse_x, mouse_y):
            player.coordinate = (0, 0)
            player.lives = 3
            player.time_dif = 0
            player.lives = player.first_lives
            player.bombs = player.first_bomb
            player.points = player.first_points
            game.reset()
            manager.part = 'play'
            audio.select.play()

        elif pause_menu[2].collidepoint(mouse_x, mouse_y):
            if save.count_saves(SAVE) < 3:
                save.save(game, player)
            else:
                manager.part = 'over_save'
            audio.select.play()

        elif pause_menu[3].collidepoint(mouse_x, mouse_y):
            manager.part = 'new'
            audio.select.play()

        elif pause_menu[4].collidepoint(mouse_x, mouse_y):
            manager.part = 'init'
            audio.select.play()

        manager.mouse_pressed = False

    return game, manager, player


def select_save(manager: Manager) -> Manager:
    """
    Handles the logic for selecting a saved game or clearing saved games in the game menu.

    Args:
        manager (Manager): An instance of the Manager class containing the current state of the game and user inputs.

    Returns:
        Manager: The updated manager instance with the new game state based on the user's selection.
    """

    save_menu = drawer.draw_select_save(manager=manager)
    saves = save.return_saves()
    save.order_saves(saves)

    buttons = [f'game {i}' for i in range(1, len(save_menu) - 1)] + ['clear', 'back']

    if manager.mouse_pressed:
        for i, button_rect in enumerate(save_menu):
            if button_rect.collidepoint(manager.mouse_x, manager.mouse_y):
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
    """
    Handles the process of overwriting a saved game in the game application.

    Args:
        manager (Manager): An instance of the Manager class that holds the current state and user inputs.

    Returns:
        Manager: An updated manager instance with potentially modified part and mouse_pressed attributes based on user interaction.
    """
    save_menu = drawer.draw_select_save('delete', player, game, manager)
    buttons = [f'game {i}' for i in range(1, len(save_menu) - 1)] + ['clear', 'back']

    if manager.mouse_pressed:
        for i, button in enumerate(save_menu):
            if button.collidepoint(manager.mouse_x, manager.mouse_y):
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
    """
    Handles the end-of-game scenario by displaying the game over screen, saving the player's score if not saved,
    and updating the game state based on user input.

    Args:
        manager (Manager): An instance of the Manager class that holds the current state of the game.

    Returns:
        Manager: The updated manager instance with the new game state.
    """
    over_menu = drawer.draw_game_over(game, player, manager)
    pygame.display.flip()

    saves = get_history()
    saved = any(save_game.name.startswith(player.name) for save_game in saves)

    if not saved:
        save.store_save(game, player)

    if manager.mouse_pressed:
        for idx, menu_option in enumerate(over_menu):
            if menu_option.collidepoint(manager.mouse_x, manager.mouse_y):
                manager.part = ['new', 'winners', 'init'][idx]
                break
        manager.mouse_pressed = False

    return manager


def winners(manager: Manager, game: Game) -> Manager:
    """
    Handles the display of the winners' screen in the game.

    Draws the winners' screen using the `drawer.draw_winners` function and checks if the user has clicked the back button to return to the initial game state.

    Args:
        manager (Manager): An instance of the `Manager` class, which holds the current state of the game and user interactions.
        game (Game): An instance of the `Game` class, which holds the current game data and state.

    Returns:
        Manager: The updated `manager` instance with potentially modified game state.
    """
    back_button = drawer.draw_winners(game)

    if manager.mouse_pressed and back_button.collidepoint(manager.mouse_x, manager.mouse_y):
        manager.part = 'init'
        audio.select.play()

    return manager


def info(manager: Manager) -> Manager:
    """
    Handles the display and interaction for the information screen in the game.

    Args:
    manager (Manager): An instance of the Manager class that holds the game state and user interactions.

    Returns:
    Manager: The updated manager instance with potentially modified state.
    """
    back_button = drawer.draw_info()

    if manager.mouse_pressed and back_button.collidepoint(manager.mouse_x, manager.mouse_y):
        manager.part = 'init'
        audio.select.play()

    return manager


def main():
    """
    The central loop of the game, handling game state transitions, user inputs, and rendering updates.
    Processes events such as key presses and mouse clicks, updates game state, and calls specific functions based on the current part of the game.
    """
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

        parts_functions = {
            'init': init,
            'new': lambda: (new(game), setattr(manager, 'part', 'play')),
            'character_sel': lambda: character_sel(manager, player),
            'load': lambda: (load(), setattr(manager, 'part', 'play')),
            'question': lambda: (question(game, manager), None),
            'winners': lambda: (winners(manager, game), None),
            'info': info,
            'play': lambda: play(manager, player),
            'pause': lambda: pause(game, manager, player),
            'select_save': select_save,
            'over_save': over_save,
            'game_over': game_over,
            'quit': lambda: setattr(manager, 'running', False)
        }

        if manager.part in parts_functions:
            result = parts_functions[manager.part]()
            if result is not None:
                if isinstance(result, Manager):
                    manager = result
                elif isinstance(result, Game):
                    game = result
                elif isinstance(result, Player):
                    player = result
                elif isinstance(result, (list, tuple)):
                    for i in result:
                        if isinstance(i, Manager):
                            manager = i
                        elif isinstance(i, Game):
                            game = i
                        elif isinstance(i, Player):
                            player = i
        else:
            manager.part = 'init'


game: Game = Game(0)
player: Player = Player('')
manager: Manager = Manager()
main()
pygame.quit()
sys.exit()