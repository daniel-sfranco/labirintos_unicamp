from typing import Any
from maze_generator import MazeGenerator
from player import Player
from os import path

def count_saves() -> int:
    if path.exists('save.che'):
        with open('save.che', 'r') as save_file:
            lines = save_file.readlines()
            game = 0
            for line in lines:
                if line[0:6] == 'game: ':
                    game += 1
    else:
        game = 0
    return game


def save(maze: MazeGenerator, player: Player):
    game = count_saves()
    if game == 0:
        type = 'w'
    else:
        type = 'a'
    with open('save.che', type) as save_file:
        save_file.write(f'game: {game + 1}\n')
        level = (maze.width - 8) // 2
        save_file.write(f'level: {level}\n')
        save_file.write(f'name: {player.name}\n')
        save_file.write(f'points: {player.points}\n')
        save_file.write(f'lives: {player.lives}\n')
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
        for line in range(maze.height * 2 - 1):
            s = ''
            for j in range(maze.width * 2 - 1):
                s += str(maze.maze[line][j]) + ' '
            save_file.write(s + '\n')


def return_saves() -> list[tuple[int, MazeGenerator, Player]]:
    games: list[tuple[int, MazeGenerator, Player]] = []
    game: tuple[int, MazeGenerator, Player] = (0, MazeGenerator(level=0, maze=[[None]]), Player(name='', skin=0))
    lines: list[str] = []
    actual_maze = []
    name = ''
    if path.exists('save.che'):
        with open('save.che', 'r') as save_file:
            lines: list[str] = save_file.readlines()
        game_number = level = bombs = lives = points = skin = -1
        name = ''
        player_position: tuple[int, int] = (0,0)
        for line in lines:
            if 'game' in line:
                if level > -1:
                    game = (game_number, MazeGenerator(level=level, maze=actual_maze), Player(name=name, skin=skin, points=points, lives=lives, bombs=bombs, coordinate=player_position))
                    games.append(game)
                game_number = int(line[6:])
            elif 'level' in line:
                level = int(line[7:])
            elif 'name' in line:
                name = line[6:]
            elif 'points' in line:
                points = int(line[8:])
            elif 'lives' in line:
                lives = int(line[7:])
            elif 'bombs' in line:
                bombs = int(line[7:])
            elif 'skin' in line:
                skin = int(line[6:])
            elif 'player position' in line:
                player_position = (int(line[18:20]), int(line[22:24]))
            else:
                actual_line: list[Any] = line.split(' ')
                for j in actual_line:
                    if j.isnumeric():
                        actual_line[actual_line.index(j)] = int(j)
                actual_maze.append(actual_line)
    return games
