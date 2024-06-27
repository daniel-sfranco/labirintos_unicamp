from player import Player
from random import choice
from constants import HISTORY
from os import path

class Student(Player):
    def __init__(self, name, level, points, coordinate):
        super().__init__(name=name, points=points, coordinate=coordinate, level=level)
        self.item = choice(['b', 'l', 't'])

def set_students(game):
    students: list[Student] = []
    if path.exists(HISTORY) and path.getsize(HISTORY) > 0:
        with open(HISTORY, 'r') as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith('name'):
                name = line[6:]
            elif line.startswith('level'):
                level = int(line[7:])
            elif line.startswith('points'):
                points = int(line[8:])
            elif line.startswith('coordinates'):
                coordinates = tuple(map(int, line[14:-2].split(', ')))
            else:
                if 'name' in locals() and level == game.level:
                    students.append(Student(name=name, level=level, points=points, coordinate=coordinates))
    if len(students) < game.level + 2:
        i = len(students)
        while i < 3:
            name = 'Student' + str(i + 1)
            level = game.level
            points = 0
            coordinate = (choice(range(len(game.maze))), choice(range(len(game.maze[0]))))
            students.append(Student(name=name, level=level, points=points, coordinate=coordinate))
            i += 1
    return students
