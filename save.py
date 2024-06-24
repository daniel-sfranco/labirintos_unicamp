from typing import Any
from game_generator import GameGenerator
from player import Player
from os import path
from constants import *

def count_saves(file=SAVE) -> int:
    if path.exists(file):
        with open(file, 'r') as save_file:
            lines = save_file.readlines()
            game = 0
            for line in lines:
                if line[0:6] == 'game: ':
                    game += 1
    else:
        game = 0
    return game


def save(game: GameGenerator, player: Player, game_number: int = 0, file=SAVE):
    num_game = count_saves(file)
    if num_game == 0:
        type = 'w'
    else:
        type = 'a'
    with open(file, type) as save_file:
        if game_number == 0:
            save_file.write(f'game: {num_game + 1}\n')
        else:
            save_file.write(f'game: {game_number}\n')
        save_file.write(f'level: {game.level}\n')
        save_file.write(f'name: {player.name}\n')
        save_file.write(f'points: {player.points}\n')
        save_file.write(f'lives: {player.lives}\n')
        save_file.write(f'time: {game.time}\n')
        save_file.write(f'bombs: {player.bombs}\n')
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


def delete_save(game_number, file=SAVE):
    with open(file, 'r') as save_file:
        lines: list[str] = save_file.readlines()
    game_level = 0
    for line in lines:
        if line[:-1] == f'game: {game_number}':
            line_index = lines.index(line)
            game_level = int(lines[line_index + 1][7:])
            break
    total_lines = (game_level + 6) * 2 + 8
    for _ in range(total_lines):
        del lines[line_index]
    with open(file, 'w') as save_file:
        for line in lines:
            save_file.write(line)


def order_saves(saves: list[tuple[int, GameGenerator, Player]], file=SAVE) -> None:
    saves = sorted(saves, key=lambda x: x[0])
    with open(file, 'w'):
        i = 1
        for game in saves:
            save(game[1], game[2], i)
            i += 1


def return_saves(file=SAVE) -> list[tuple[int, GameGenerator, Player]]:
    games: list[tuple[int, GameGenerator, Player]] = []
    game: tuple[int, GameGenerator, Player] = (0, GameGenerator(level=0, maze=[[None]]), Player(name='', skin=0))
    lines: list[str] = []
    actual_maze = []
    name = ''
    if path.exists(file):
        with open(file, 'r') as save_file:
            lines: list[str] = save_file.readlines()
        game_number = level = bombs = lives = points = time = skin = row = -1
        player_position: tuple[int, int] = (0,0)
        num_games = count_saves(SAVE)
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
                skin = int(line[6:])
            elif 'player position' in line:
                player_position = (int(line[18:20]), int(line[22:24]))
            else:
                row += 1
                actual_line: list[Any] = line.split(' ')
                for j in actual_line:
                    if j.isnumeric():
                        actual_line[actual_line.index(j)] = int(j)
                actual_line.pop()
                actual_maze.append(actual_line)
                if row == (level + 6) * 2 - 2:
                    if level > -1 and len(games) < num_games:
                        game = (game_number, GameGenerator(level=level, maze=actual_maze), Player(name=name, skin=skin, points=points, lives=lives, bombs=bombs, coordinate=player_position))
                        games.append(game)
                        actual_maze = []
                        game_number = level = bombs = lives = points = skin = row = -1
                        actual_line = []
    return games


def store_save(game: GameGenerator, player: Player) -> None:
    games = return_saves()
    for g in games:
        if g[1] == game and g[2] == player:
            game_number = g[0]
            break
    save(game, player, file='history.che')
    if 'game_number' in locals():
        delete_save(game_number)

if __name__ == "__main__":
    with open('save.che', 'w') as save_file:
        pass
    for i in range(1, 4):
        maze = GameGenerator(i)
        player = Player('test_player', 0)
        save(maze, player)
    order_saves(return_saves())
    #delete_save(1)
