from maze_generator import MazeGenerator
from player import Player
from os import path

def count_saves() -> int:
    if path.exists('save.che'):
        with open('save.che', 'r') as save_file:
            lines = save_file.readlines()
            game = 0
            for i in lines:
                if i[0:6] == 'game: ':
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
        for i in player.coordinate:
            if i // 10 == 0:
                c += '0' + str(i)
            else:
                c += str(i)
            c += ', '
        c = c[:-2] + ')'
        save_file.write(f'player position: {c}\n')
        for i in range(maze.height * 2 - 1):
            s = ''
            for j in range(maze.width * 2 - 1):
                s += str(maze.maze[i][j]) + ' '
            save_file.write(s + '\n')


def return_saves() -> list[dict]:
    games: list[list[int, MazeGenerator, Player]] = []
    game: list[int, MazeGenerator, Player] = []
    num_games = count_saves()
    actual_player = {}
    actual_maze = []
    name = ''
    if path.exists('save.che'):
        with open('save.che', 'r') as save_file:
            lines = save_file.readlines()
        level = bombs = lives = points = skin = game = -1
        name = ''
        player_position = (0,0)
        for i in lines:
            if 'game' in i:
                if level > -1:
                    width = height = (level * 2 + 8)
                    game.append([game, MazeGenerator(width=width, height=height, maze=maze), Player(name=name, skin=skin, points=points, lives=lives, bombs=bombs, coordinate=player_position)])
                game = int(i[6:])
            elif 'level' in i:
                level = int(lines[i][7:])
            elif 'name' in i:
                name = lines[i][6:]
            elif 'points' in i:
                points = int(lines[i][8:])
            elif 'lives' in i:
                lives = int(lines[i][7:])
            elif 'bombs' in i:
                bombs = int(lines[i][7:])
            elif 'skin' in i:
                skin = int(lines[i][6:])
            elif 'player position' in i:
                player_position = tuple(int(i[18:20]), int(i[22:24]))

if __name__ == '__main__':
    maze = MazeGenerator(10, 10, 0)
    player = Player('save_test', 0)
    save(maze, player)