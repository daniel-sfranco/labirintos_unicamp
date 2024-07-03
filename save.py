from typing import Any
from game_generator import Game
from player import Player
from os import path
from constants import SAVE, HISTORY, CHARACTERS
from student import get_history, Student


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


def save(game: Game, player: Player, game_number: int = 0, file=SAVE):
    num_game = count_saves(file)
    if num_game == 0:
        type = 'w'
    else:
        type = 'a'
    if file == SAVE:
        saves = return_saves()
        for save in saves:
            if save[2].name == player.name:
                delete_save(save)
                num_game -= 1
                break
        with open(file, type) as save_file:
            if game_number == 0:
                save_file.write(f'game: {num_game + 1}\n')
            else:
                save_file.write(f'game: {game_number}\n')
            save_file.write(f'skin: {player.skin}')
            save_file.write(f'level: {game.level}\n')
            save_file.write(f'name: {player.name}\n')
            save_file.write(f'points: {player.points}\n')
            save_file.write(f'lives: {player.lives}\n')
            save_file.write(f'time: {game.time}\n')
            save_file.write(f'bombs: {player.bombs}\n')
            if isinstance(player.skin, int):
                save_file.write(f'skin: {CHARACTERS[player.skin]}\n')
            else:
                save_file.write(f'skin: {player.skin}\n')
            c = '('
            for line in player.coordinate:
                if line // 10 == 0:
                    c += '0' + str(line)
                else:
                    c += str(line)
                c += ', '
            c = c[:-2] + ')'
            save_file.write(f'player position: {c}\n')
            for line in range(len(game.maze)):
                s = ''
                for j in range(len(game.maze[line])):
                    s += str(game.maze[line][j]) + ' '
                save_file.write(s + '\n')
            for line in range(len(game.first_maze)):
                s = ''
                for j in range(len(game.first_maze[line])):
                    s += str(game.first_maze[line][j]) + ' '
                save_file.write(s + '\n')
    elif file == HISTORY:
        game_number = count_saves(HISTORY) + 1
        with open(file, type) as history_file:
            history_file.write(f'game: {game_number}\n')
            history_file.write(f'name: {player.name}\n')
            history_file.write(f'skin: {player.skin}\n')
            history_file.write(f'level: {game.level}\n')
            history_file.write(f'points: {player.points}\n')
            history_file.write(f'coordinates: {player.coordinate}\n')


def delete_save(game_number, file=SAVE):
    with open(file, 'r') as save_file:
        lines: list[str] = save_file.readlines()
    game_level = 0
    for line in lines:
        if line[:-1] == f'game: {game_number}':
            line_index = lines.index(line)
            game_level = int(lines[line_index + 1][7:])
            break
    total_lines = ((game_level + 6) * 2 - 1) * 2 + 8
    if 'line_index' in locals():
        for _ in range(total_lines):
            del lines[line_index]
    with open(file, 'w') as save_file:
        for line in lines:
            save_file.write(line)


def order_saves(saves: list[tuple[int, Game, Player]], file=SAVE) -> None:
    saves = sorted(saves, key=lambda x: x[0])
    with open(file, 'w'):
        i = 1
        for game in saves:
            save(game[1], game[2], i)
            i += 1


def return_saves(file=SAVE) -> list[tuple[int, Game, Player]]:
    games: list[tuple[int, Game, Player]] = []
    game: tuple[int, Game, Player] = (0, Game(level=0), Player(name=''))
    lines: list[str] = []
    actual_maze = []
    name = ''
    if path.exists(file):
        with open(file, 'r') as save_file:
            lines: list[str] = save_file.readlines()
        game_number = level = bombs = lives = points = row = -1
        skin = ''
        player_position: tuple[int, int] = (0, 0)
        num_games = count_saves(file)
        first_maze = False
        for line in lines:
            if 'game' in line:
                game_number = int(line[6:])
            elif 'level' in line:
                level = int(line[7:])
            elif 'name' in line:
                name = line[6:-1]
            elif 'points' in line:
                points = int(line[8:])
            elif 'lives' in line:
                lives = int(line[7:])
            elif 'time' in line:
                time = int(line[6:])
            elif 'bombs' in line:
                bombs = int(line[7:])
            elif 'skin' in line:
                skin = line[6:-1]
            elif 'player position' in line:
                player_position = (int(line[18:20]), int(line[22:24]))
            else:
                if not isinstance(first_maze, list):
                    row += 1
                    actual_line: list[Any] = line.split(' ')
                    for j in actual_line:
                        if j.isnumeric():
                            actual_line[actual_line.index(j)] = int(j)
                    actual_line.pop()
                    actual_maze.append(actual_line)
                    if row == (level + 6) * 2 - 2:
                        first_maze = []
                        row = -1
                else:
                    row += 1
                    actual_line: list[Any] = line.split(' ')
                    for j in actual_line:
                        if j.isnumeric():
                            actual_line[actual_line.index(j)] = int(j)
                    actual_line.pop()
                    first_maze.append(actual_line)
                    if row == (level + 6) * 2 - 2:
                        if level > -1 and len(games) < num_games:
                            act_game = Game(level=level, maze=actual_maze, first_maze=first_maze, act_time=time)
                            act_player = Player(name=name, skin=skin, points=points, lives=lives, bombs=bombs, coordinate=player_position, level=level)
                            game = (game_number, act_game, act_player)
                            games.append(game)
                            actual_maze = []
                            first_maze = False
                            game_number = level = bombs = lives = points = row = -1
                            skin = ''
                            actual_line = []
    return games


def store_save(game: Game, player: Player) -> None:
    games = return_saves()
    for g in games:
        if g[1] == game and g[2] == player:
            game_number = g[0]
            break
    students = get_history()
    valid = True
    for student in students:
        if student.name == player.name and student.skin == player.skin and student.points == player.points and student.coordinate == player.coordinate and student.level == player.level:
            valid = False
    if valid:
        save(game, player, file=HISTORY)
    if 'game_number' in locals():
        delete_save(game_number)


if __name__ == "__main__":
    game = Game(1)
    player = Player('test_player')
    game.maze[2][0] = 'b'
    save(game, player)
    order_saves(return_saves())
    # delete_save(1)
