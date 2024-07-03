from player import Player
from random import choice
from constants import HISTORY
from os import path


class Student(Player):
    def __init__(self, name: str = '', level: int = 0, points: int = 0, coordinate: tuple[int, int] = (-1, -1), num: int = 0, lives: int = 3, bombs: int = 0):
        super().__init__(name=name, points=points, coordinate=coordinate, level=level, skin='ghost')
        self.num = num
        self.possibilities = ['c']
        if lives < 5:
            self.possibilities.append('l')
        if bombs < 5:
            self.possibilities.append('b')
        self.item = choice(self.possibilities)


def get_students(game) -> list[Student]:
    students: list[Student] = []
    coordinate: tuple[int, int] = (0, 0)
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
                coordinate = (coordinates[0], coordinates[1])
            else:
                num = int(line[6:])
                if 'name' in locals() and level == game.level and coordinates != (0, 0):
                    students.append(Student(name=name, level=level, points=points, coordinate=coordinate, num=num))
    if len(students) < game.level:
        for i in range(len(game.maze)):
            for j in range(len(game.maze[i])):
                if game.maze[i][j] == 's':
                    valid = True
                    for student in students:
                        if (i, j) == student.coordinate:
                            valid = False
                    if valid is True:
                        students.append(Student(name='Student', level=game.level, points=0, coordinate=(i, j), num=len(students) + 1))
    return students


def set_students(game):
    students = get_students(game)

    if len(students) < game.level // 2 or len(students) == 0:
        i = len(students)
        while True:
            num = len(students) + 1
            name = 'Student' + str(i + 1)
            level = game.level
            points = 0
            coord_x = choice(range(len(game.maze)))
            coord_y = choice(range(len(game.maze[0])))
            coordinate = (coord_x, coord_y)
            if coordinate == (len(game.maze), len(game.maze[-1])):
                continue
            students.append(Student(name=name, level=level, points=points, coordinate=coordinate, num=num))
            i += 1
            if i >= game.level // 2:
                break
    elif len(students) > game.level // 2:
        students = sorted(students, key=lambda student: student.num, reverse=True)
        students = students[:game.level // 2]
    return students


def get_history(game):
    students: list[Student] = []
    if path.exists(HISTORY) and path.getsize(HISTORY) > 0:
        with open(HISTORY, 'r') as file:
            lines = file.readlines()
        count = 0
        for line in lines:
            if line.startswith('name'):
                name = line[6:]
                count += 1
            elif line.startswith('level'):
                level = int(line[7:])
                count += 1
            elif line.startswith('points'):
                points = int(line[8:])
                count += 1
            if count == 3:
                students.append(Student(name=name, level=level, points=points))
                count = 0

    students = sorted(students, key=lambda x: x.points, reverse=True)
    return students
