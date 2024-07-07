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
            pygame.mixer.music.stop()
            manager.is_music_playing = False
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

    elif manager.part == 'info':
        if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
            manager.part = 'init'
        elif event.key == pygame.K_RIGHT and manager.info_type == 'story':
            manager.info_type = 'info'
            audio.select.play()
        elif event.key == pygame.K_LEFT and manager.info_type == 'info':
            manager.info_type = 'story'
            audio.select.play()
    return manager


def init() -> Manager:
    if not manager.is_music_playing:
        audio.music_setter('dungeon_level')
        manager.is_music_playing = True
    
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


def new(name: str, skin: str, player: Player = Player('')) -> tuple[Game, Player]:
    """
    Initializes a new game level, resets the player's position, redraws the maze, updates the display, and adjusts the game's time difference.

    Args:
        game (Game): An instance of the Game class representing the current game state.

    Returns:
        Game: The newly created Game instance with the updated level and time difference.
    """
    new_game = Game(game.level + 1)
    if player.name == '':
        player = Player(name=name, skin=skin)
    else:
        player.points += game.points
        player.time_dif = 0
        player.first_points = player.points
        player.coordinate = (0,0)
    drawer.draw_maze(player, new_game, manager)
    pygame.display.flip()
    new_game.time_dif = TIME - new_game.time
    return new_game, player


def character_sel():
    """
    Handles the character selection process in the game.

    Args:
    - manager: An instance of the Manager class that tracks the game's state and user inputs.
    - player: An instance of the Player class representing the current player.

    Returns:
    - Updated manager object with the new game state.
    - Updated player object with the selected character and name.
    """
    global game, player
    if not manager.is_music_playing:
        audio.music_setter('dungeon_level')
        manager.is_music_playing = True
    buttons_char, arrows, input_box, skin_choice = drawer.draw_character_sel(manager)

    if manager.mouse_pressed:
        mouse_x, mouse_y = manager.mouse_x, manager.mouse_y

        if buttons_char[0].collidepoint(mouse_x, mouse_y):
            manager.part = 'init'
            audio.select.play()
        elif buttons_char[1].collidepoint(mouse_x, mouse_y):
            if manager.user_input != "":
                name = manager.user_input
            else:
                history = get_history()
                name = f'Jogador {len(history)}'
            game, player = new(name, skin_choice)
            manager.part = 'play'
            pygame.mixer.music.stop()
            manager.is_music_playing = False
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

    elif manager.key_pressed:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            manager.is_music_playing = False
            audio.select.play()
            manager.key_pressed = False

            if manager.user_input != "":
                name = manager.user_input
            else:
                history = get_history()
                name = f'Jogador {len(history)}'
            game, player = new(name, skin_choice)
            manager.part = 'play'
            pygame.mixer.music.stop()
            manager.is_music_playing = False


def load() -> tuple[Game, Player]:
    """
    Retrieves a saved game and player state from a list of saved games,
    draws the maze on the SCREEN, updates the game's time difference, and returns the game and player objects.
    """
    global game, player
    games = save.return_saves()
    index = manager.game_number - 1
    game, player = games[index][1], games[index][2]
    drawer.draw_maze(player, game, manager)
    pygame.display.flip()
    game.time_dif = game.time - TIME

    return game, player


def question() -> None:
    """
    Handles presenting a question to the player, capturing their answer, and updating the game state based on correctness.

    Args:
        game (Game): An instance of the Game class representing the current game state.
        manager (Manager): An instance of the Manager class managing the game state and player interactions.

    Returns:
        tuple[Game, Manager]: Updated Game and Manager instances.
    """

    if not manager.questioned:
        manager.chosen_answer = ''
        manager.num_question = random.randint(1, 100)
        manager.question = Question(manager.num_question, manager.questioned)
        manager.question_type = game.maze[manager.question_giver[0]][manager.question_giver[1]]
        manager.questioned = True
        return None
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
        # game.time_dif += trunc(time.perf_counter() - manager.start_question)
        manager.chosen_answer = ''
        pygame.time.delay(1500)


def play() -> tuple[Game, Manager, Player]:
    # Calculate time passed and update game time and points
    global player, game
    if not manager.is_music_playing:
        audio.music_setter('ancient_shrine')
        manager.is_music_playing = True
    pygame.mixer.music.unpause()

    passed = trunc(time.perf_counter() - game.start) - game.time_dif - player.time_dif
    game.time = TIME - passed
    if game.act_points > 0:
        game.points = round(game.level * game.act_points * (1 - (passed / TIME)) * 100)

    # Handle bomb detonation
    if game.bomb_start != 0 and game.bomb_coords != (-1, -1):
        game.bomb_time = BOMB_TIME - trunc(time.perf_counter() - game.bomb_start)
        game.bomb_animation_time = BOMB_TIME - (time.perf_counter() - game.bomb_start)
        if game.bomb_time <= 0:
            player = game.detonate(player, game.bomb_coords)
            manager.key_pressed = False
            manager.bomb_sprite.current_sprite = 0
            game.bomb_start = 0
            game.bomb_coords = (-1, -1)

    # Check player lives and game over conditions
    if game.time <= 0:
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
        pygame.mixer.music.stop()
        manager.is_music_playing = False

    # Handle player movement and interactions with students and teachers
    manager.question_giver = (-1, -1)
    coord = player.coordinate
    next_coordinate = player.move_player(game)
    move = coord != next_coordinate

    for student in game.students:
        if student.coordinate == next_coordinate and move:
            manager.part = 'question'
            manager.question_giver = student.coordinate
            manager.start_question = time.perf_counter()
            poss_items = ['b', 'c', 'l']
            if student.item == 'l' and player.lives >= 5:
                poss_items.remove('l')
            elif student.item == 'b' and player.bombs >= 5:
                poss_items.remove('b')
            student.item = random.choice(poss_items)
            return game, manager, player

    for teacher in game.teachers:
        game.maze = teacher.move(player, game, move)
        if abs(teacher.coordinate[0] - player.coordinate[0]) <= 1 and abs(teacher.coordinate[1] - player.coordinate[1]) <= 1:
            manager.part = 'question'
            manager.question_giver = teacher.coordinate
            manager.start_question = time.perf_counter()
        elif teacher.coordinate == next_coordinate and move:
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
            game.maze[player.coordinate[0]][player.coordinate[1]] += 'x'
            game.bomb_coords = player.coordinate

    # Check for level completion
    if next_coordinate == (-1, -1):
        game, _ = new(player.name, player.skin, player)
        audio.level_complete.play()

    return game, manager, player


def pause() -> tuple[Game, Manager, Player]:
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
    global game
    pause_menu = drawer.draw_pause_menu(player, game, manager)
    pygame.display.flip()
    if manager.is_music_playing:
        pygame.mixer.music.pause()

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
            manager.part = 'character_sel'
            game = Game(FIRST_LEVEL - 1)
            pygame.mixer.music.stop()
            manager.is_music_playing = False
            audio.select.play()

        elif pause_menu[4].collidepoint(mouse_x, mouse_y):
            manager.part = 'init'
            game = Game(FIRST_LEVEL - 1)
            pygame.mixer.music.stop()
            manager.is_music_playing = False
            audio.select.play()

        manager.mouse_pressed = False

    return game, manager, player


def select_save() -> Manager:
    """
    Handles the logic for selecting a saved game or clearing saved games in the game menu.

    Args:
        manager (Manager): An instance of the Manager class containing the current state of the game and user inputs.

    Returns:
        Manager: The updated manager instance with the new game state based on the user's selection.
    """
    global game, player
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
                    manager.game_number = int(buttons[i].replace('game ', ''))
                    manager.mouse_pressed = False
                    game, player = load()
                    pygame.mixer.music.stop()
                    manager.is_music_playing = False
                    manager.part = 'play'
                    pygame.mixer.music.stop()
                    manager.is_music_playing = False
                    break

    return manager


def over_save() -> Manager:
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
                    if os.path.exists(SAVE):
                        os.remove(SAVE)
                else:
                    game_number = int(buttons[i].replace('game ', ''))
                    save.delete_save(game_number)
                    save.save(game, player, game_number)
                    save.order_saves(save.return_saves())
                    manager.part = 'pause'
                    manager.mouse_pressed = False
                    break

    return manager


def game_over() -> Manager:
    """
    Handles the end-of-game scenario by displaying the game over SCREEN, saving the player's score if not saved,
    and updating the game state based on user input.

    Args:
        manager (Manager): An instance of the Manager class that holds the current state of the game.

    Returns:
        Manager: The updated manager instance with the new game state.
    """
    if not manager.is_music_playing:
        audio.music_setter('castle-of-athanasius')
        manager.is_music_playing = True

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
                pygame.mixer.music.stop()
                manager.is_music_playing = False
                break
        manager.mouse_pressed = False
        pygame.mixer.music.stop()
        audio.music_setter('dungeon_level')

    return manager


def winners() -> Manager:
    """
    Handles the display of the winners' SCREEN in the game.

    Draws the winners' SCREEN using the `drawer.draw_winners` function and checks if the user has clicked the back button to return to the initial game state.

    Args:
        manager (Manager): An instance of the `Manager` class, which holds the current state of the game and user interactions.
        game (Game): An instance of the `Game` class, which holds the current game data and state.

    Returns:
        Manager: The updated `manager` instance with potentially modified game state.
    """
    if not manager.is_music_playing:
        audio.music_setter('dungeon_level')
        manager.is_music_playing = True
    back_button = drawer.draw_winners()

    if manager.mouse_pressed and back_button.collidepoint(manager.mouse_x, manager.mouse_y):
        manager.part = 'init'
        audio.select.play()

    return manager


def info() -> Manager:
    """
    Handles the display and interaction for the information SCREEN in the game.

    Args:
    manager (Manager): An instance of the Manager class that holds the game state and user interactions.

    Returns:
    Manager: The updated manager instance with potentially modified state.
    """
    buttons = drawer.draw_info(manager.info_type)

    if manager.mouse_pressed:
        if buttons[0].collidepoint(manager.mouse_x, manager.mouse_y):
            manager.part = 'init'
            manager.info_type = 'story'
            audio.select.play()
        elif buttons[1].collidepoint(manager.mouse_x, manager.mouse_y):
            if manager.info_type == 'story':
                manager.info_type = 'info'
            else:
                manager.info_type = 'story'
            audio.select.play()
    return manager


def main():
    """
    The central loop of the game, handling game state transitions, user inputs, and rendering updates.
    Processes events such as key presses and mouse clicks, updates game state, and calls specific functions based on the current part of the game.
    """
    global manager, game, player
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
            'character_sel': character_sel,
            'question': question,
            'play': play,
            'pause': pause,
            'select_save': select_save,
            'over_save': over_save,
            'game_over': game_over,
            'winners': winners,
            'info': info,
            'quit': lambda: setattr(manager, 'running', False)
        }
        if manager.part in parts_functions:
            result = parts_functions[manager.part]()
            if result is not None:
                if isinstance(result, Manager):
                    del manager
                    manager = result
                elif isinstance(result, Game):
                    del game
                    game = result
                elif isinstance(result, Player):
                    del player
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

game: Game = Game(FIRST_LEVEL - 1)
player: Player = Player('')
manager: Manager = Manager()

main()
pygame.quit()
sys.exit()
