from random import randint
from pygame import time
from player import Player


class Teacher:
    def __init__(self, game, first_coordinate: tuple[int, int] = (-1, -1), coordinate: tuple[int, int] = (-1, -1)) -> None:
        if first_coordinate == (-1, -1) and coordinate == (-1, -1):
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
            self.coordinate: tuple[int, int] = coordinate
            self.first_coordinate: tuple[int, int] = first_coordinate

    def move(self, player: Player, game):
        free = False
        next_coord: tuple[int, int] = (-1, -1)
        if self.coordinate[0] == player.coordinate[0]:
            if self.coordinate[1] > player.coordinate[1]:
                free = game.maze[self.coordinate[0]][self.coordinate[1] - 1] == 0
                if free:
                    next_coord = (self.coordinate[0], self.coordinate[1] - 1)
            elif self.coordinate[1] < player.coordinate[1]:
                free = game.maze[self.coordinate[0]][self.coordinate[1] + 1] == 0
                if free:
                    next_coord = (self.coordinate[0], self.coordinate[1] + 1)
        elif self.coordinate[1] == player.coordinate[1]:
            if self.coordinate[0] > player.coordinate[0]:
                free = game.maze[self.coordinate[0] - 1][self.coordinate[1]] == 0
                if free:
                    next_coord = (self.coordinate[0] - 1, self.coordinate[1])
            elif self.coordinate[0] < player.coordinate[0]:
                free = game.maze[self.coordinate[0] + 1][self.coordinate[1]] == 0
                if free:
                    next_coord = (self.coordinate[0] + 1, self.coordinate[1])
        if free:
            game.maze[self.coordinate[0]][self.coordinate[1]] = 0
            game.maze[next_coord[0]][next_coord[1]] = 't'
            self.coordinate = next_coord
            time.delay(250)
        return game.maze


def set_teachers(game):
    teachers = []
    teacher_pos = []
    for y in range(len(game.maze)):
        for x in range(len(game.maze[y])):
            if game.maze[y][x] == 't':
                teacher_pos.append((y, x))
    if len(teacher_pos) > 0:
        for pos in teacher_pos:
            teachers.append(Teacher(game, first_coordinate=pos, coordinate=pos))
    else:
        for _ in range(game.level):
            teachers.append(Teacher(game))
    return teachers
