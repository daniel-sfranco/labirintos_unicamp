from maze_generator import MazeGenerator
from player import Player
from drawer import set_screen
from os import path

def count_saves() -> int:
    if path.exists('save.che'):
        with open('save.che', 'r') as save_file:
            lines = save_file.readlines()
            games = 0
            for i in lines:
                if i[0:6] == 'game: ':
                    games += 1
    else:
        games = 0
    return games


def save(maze: MazeGenerator, player: Player):
    games = count_saves()
    if games == 0:
        type = 'w'
    else:
        type = 'a'
    with open('save.che', type) as save_file:
        save_file.write('\n')
        save_file.write(f'game: {games + 1}\n')
        for i in range(maze.height * 2 - 1):
            s = ''
            for j in range(maze.width * 2 - 1):
                s += str(maze.maze[i][j]) + ' '
            s = s[:-1]
            save_file.write(s + '\n')
        level = (maze.width - 8) // 2
        save_file.write(f'level: {level}\n')
        save_file.write(f'name: {player.name}\n')
        save_file.write(f'points: {player.points}\n')
        save_file.write(f'lives: {player.lives}\n')
        save_file.write(f'bombs: {player.bombs}\n')
        save_file.write(f'skin: {player.skin}\n')
        save_file.write(f'player position: {player.coordinate}\n')

if __name__ == '__main__':
    maze = MazeGenerator(10, 10, 0)
    player = Player('save_test', 0)
    save(maze, player)