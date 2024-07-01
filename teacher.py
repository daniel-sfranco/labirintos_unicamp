from random import randint
from pygame import time


class Teacher:
    def __init__(self, game, first_coordinate: tuple = (), coordinate: tuple = ()) -> None:
        if first_coordinate == () and coordinate == ():
            while True:
                x = randint(1, len(game.maze)) - 1
                y = randint(1, len(game.maze[0])) - 1
                self.coordinate = (x, y)
                if self.coordinate == (len(game.maze) - 1, len(game.maze[0]) - 1):
                    continue
                elif game.maze[self.coordinate[0]][self.coordinate[1]] != 0:
                    continue
                else:
                    self.first_coordinate = self.coordinate
                    break
        else:
            self.coordinate = coordinate
            self.first_coordinate = first_coordinate

    def move(self, player, game):
        free = False
        next_coord = (-1, -1)
        if self.coordinate[0] == player.coordinate[0]:
            if self.coordinate[1] > player.coordinate[1]:
                free = game.maze[self.coordinate[0]][self.coordinate[1] - 1] == 0
                if free:
                    next_coord = [self.coordinate[0], self.coordinate[1] - 1]
            elif self.coordinate[1] < player.coordinate[1]:
                free = game.maze[self.coordinate[0]][self.coordinate[1] + 1] == 0
                if free:
                    next_coord = [self.coordinate[0], self.coordinate[1] + 1]
        elif self.coordinate[1] == player.coordinate[1]:
            if self.coordinate[0] > player.coordinate[0]:
                free = game.maze[self.coordinate[0] - 1][self.coordinate[1]] == 0
                if free:
                    next_coord = [self.coordinate[0] - 1, self.coordinate[1]]
            elif self.coordinate[0] < player.coordinate[0]:
                free = game.maze[self.coordinate[0] + 1][self.coordinate[1]] == 0
                if free:
                    next_coord = [self.coordinate[0] + 1, self.coordinate[1]]
        if free:
            game.maze[self.coordinate[0]][self.coordinate[1]] = 0
            game.maze[next_coord[0]][next_coord[1]] = 't'
            self.coordinate = next_coord
            time.delay(250)
        return game.maze


def set_teachers(game):
    teachers = []
    for _ in range(game.level):
        teachers.append(Teacher(game))
    return teachers


def get_teachers(game):
    teachers = []
    for i in range(len(game.maze)):
        for j in range(len(game.maze[i])):
            if game.maze[i][j] == 't':
                teachers.append(Teacher(game, (i, j), (i, j)))
    return teachers
