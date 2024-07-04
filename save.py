from game_generator import Game
from player import Player
from os import path
from constants import SAVE, HISTORY, CHARACTERS
from student import get_history


def count_saves(file: str = SAVE) -> int:
    if path.exists(file):
        with open(file, 'r') as save_file:
            lines = save_file.readlines()
            game = 0
            for line in lines:
                if line[0:6] == 'name: ':
                    game += 1
    else:
        game = 0
    return game


def save(game: Game, player: Player, game_number: int = 0, file: str = SAVE) -> None:
    """
    Save the current state of the game and player to a file.

    Args:
        game (Game): An instance of the Game class representing the current game state.
        player (Player): An instance of the Player class representing the current player state.
        game_number (int, optional): An optional integer representing the game number to save. Defaults to 0.
        file (str, optional): An optional string representing the file to save to. Defaults to SAVE.
    """
    num_game = count_saves(file)
    mode = 'w' if num_game == 0 else 'a'

    if file == SAVE:
        saves = return_saves()
        for save_data in saves:
            if save_data[2].name == player.name:
                delete_save(save_data[0])
                num_game -= 1
                break

        with open(file, mode) as save_file:
            game_num = num_game + 1 if game_number == 0 else game_number
            save_file.write(f'game: {game_num}\n')
            save_file.write(f'level: {game.level}\n')
            save_file.write(f'name: {player.name}\n')
            save_file.write(f'points: {player.points}\n')
            save_file.write(f'lives: {player.lives}\n')
            save_file.write(f'time: {game.time}\n')
            save_file.write(f'bombs: {player.bombs}\n')
            save_file.write(f'skin: {CHARACTERS[player.skin] if isinstance(player.skin, int) else player.skin}\n')
            coordinates = '(' + ', '.join([f'{line:02}' for line in player.coordinate]) + ')'
            save_file.write(f'player position: {coordinates}\n')

            for maze_row in game.maze:
                save_file.write(' '.join(map(str, maze_row)) + '\n')

            for init_maze_row in game.init_maze:
                save_file.write(' '.join(map(str, init_maze_row)) + '\n')

    elif file == HISTORY:
        game_number = count_saves(HISTORY) + 1
        with open(file, mode) as history_file:
            history_file.write(f'game: {game_number}\n')
            history_file.write(f'name: {player.name}\n')
            history_file.write(f'skin: {player.skin}\n')
            history_file.write(f'level: {game.level}\n')
            history_file.write(f'points: {player.points}\n')
            history_file.write(f'coordinates: {player.coordinate}\n')


def delete_save(game_number: int, file: str = SAVE) -> None:
    """
    Remove the save data for a specific game number from a save file.

    Args:
        game_number (int): The number of the game whose save data needs to be deleted.
        file (str): The path to the save file (default is 'SAVE').
    """
    with open(file, 'r') as save_file:
        lines: list[str] = save_file.readlines()

    game_level = 0
    for index, line in enumerate(lines):
        if line.rstrip() == f'game: {game_number}':
            game_level = int(lines[index + 1][7:])
            del lines[index:index + game_level * 4 + 31]
            break

    with open(file, 'w') as save_file:
        for line in lines:
            save_file.write(line)


def order_saves(saves: list[tuple[int, Game, Player]], file: str = 'SAVE') -> None:
    """
    Sorts a list of game saves by their game number and writes them back to a file in the sorted order.

    Args:
        saves (List[Tuple[int, Game, Player]]): A list of tuples containing a game number, a Game instance, and a Player instance.
        file (str): An optional string specifying the file to save to, defaulting to 'SAVE'.

    Returns:
        None
    """
    saves = sorted(saves, key=lambda x: x[0])
    with open(file, 'w'):
        game_number = 1
        for game_save in saves:
            save(game_save[1], game_save[2], game_number)
            game_number += 1


def return_saves(file: str = SAVE) -> list[tuple[int, Game, Player]]:
    """
    Reads a save file and reconstructs a list of saved game states.

    Args:
        file (str): The path to the save file (default is 'SAVE').

    Returns:
        List[Tuple[int, Game, Player]]: A list of tuples, each containing a game number, a Game object, and a Player object.
    """
    games: list[tuple[int, Game, Player]] = []
    actual_maze = []
    name = ''

    if path.exists(file):
        with open(file, 'r') as save_file:
            lines: list[str] = save_file.readlines()
        game_number = level = bombs = lives = points = row = -1
        skin = ''
        player_position: tuple[int, int] = (-1, -1)
        num_games = count_saves(file)
        init_maze = False

        for i in lines:
            line = i.rstrip()

            if 'game' in line:
                game_number = int(line[6:])
            elif 'level' in line:
                level = int(line[7:])
            elif 'name' in line:
                name = line[6:]
            elif 'points' in line:
                points = int(line[8:])
            elif 'lives' in line:
                lives = int(line[7:])
            elif 'time' in line:
                time = int(line[6:])
            elif 'bombs' in line:
                bombs = int(line[7:])
            elif 'skin' in line:
                skin = line[6:]
            elif 'player position' in line:
                player_position = (int(line[18:20]), int(line[22:24]))
            else:
                if not isinstance(init_maze, list):
                    row += 1
                    actual_line = [int(j) if j.isnumeric() else j for j in line.split(' ')]
                    actual_maze.append(actual_line)

                    if row == level * 2 + 10:
                        init_maze = []
                        row = -1
                else:
                    row += 1
                    actual_line = [int(j) if j.isnumeric() else j for j in line.split(' ')]
                    init_maze.append(actual_line)

                    if row == level * 2 + 10:
                        if level > -1 and len(games) < num_games:
                            act_game = Game(level=level, maze=actual_maze, init_maze=init_maze, act_time=time)
                            act_player = Player(name=name, skin=skin, points=points, lives=lives, bombs=bombs, coordinate=player_position, level=level)
                            game = (game_number, act_game, act_player)
                            games.append(game)
                            actual_maze = []
                            init_maze = False
                            game_number = level = bombs = lives = points = row = -1
                            skin = ''
                            actual_line = []

    return games


def store_save(game: Game, player: Player) -> None:
    """
    Check if the current game and player state already exist in the saved games.
    If they do, retrieve the game number. Verify if the player's history is unique,
    and if so, save the game state to the history file. Finally, if the game number
    was found, delete the existing save for that game number.

    :param game: An instance of the Game class representing the current game state.
    :param player: An instance of the Player class representing the current player state.
    :return: None
    """
    games = return_saves()
    game_number = None

    for g in games:
        if g[1] == game and g[2] == player:
            game_number = g[0]
            break

    students = get_history()
    valid = all(student != player for student in students)

    if valid:
        save(game, player, file=HISTORY)

    if game_number is not None:
        delete_save(game_number)


if __name__ == "__main__":
    num_games = count_saves()
    game = Game(num_games + 1)
    player = Player(f'test_player{num_games + 1}')
    save(game, player)
    saves = return_saves()
