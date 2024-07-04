from player import Player
from random import choice
from constants import HISTORY
from os import path


class Student(Player):
    """
    Represents a student character in the game.

    Attributes:
    - num: An integer representing the student's number.
    - possibilities: A list of possible items the student can possess.
    - last_skin: The last skin used by the student.
    - item: The item chosen randomly from the possibilities.
    """

    def __init__(self, name: str = '', level: int = 0, points: int = 0, coordinates: tuple[int, int] = (-1, -1), game: int = 0, lives: int = 3, bombs: int = 0, skin: str = 'superhero'):
        """
        Initializes a student with specific attributes and determines the possible items a student can possess based on their lives and bombs.

        Args:
        - name: The name of the student.
        - level: The level of the student.
        - points: The points of the student.
        - coordinate: The coordinate of the student.
        - num: The number of the student.
        - lives: The number of lives of the student.
        - bombs: The number of bombs of the student.
        - skin: The skin of the student.
        """
        super().__init__(name=name, points=points, coordinate=coordinates, level=level, skin='ghost')
        self.num = game
        self.possibilities = ['c']
        self.last_skin = skin.rstrip()
        if lives < 5:
            self.possibilities.append('l')
        if bombs < 5:
            self.possibilities.append('b')
        self.item = choice(self.possibilities)


def get_students(game) -> list[Student]:
    """
    Retrieves a list of Student objects for a game.
    Reads from a history file to restore previous student states if available,
    and if not enough students are found, generates new ones based on the current game state.

    :param game: An object representing the current game state, which includes the game level and maze layout.
    :return: A list of Student objects representing the students in the game.
    """
    students: list[Student] = []
    coordinate: tuple[int, int] = (0, 0)

    if path.exists(HISTORY) and path.getsize(HISTORY) > 0:
        with open(HISTORY, 'r') as file:
            lines = file.readlines()

        for line in lines:
            data = line.strip().split(':')
            if data[0] == 'name':
                name = data[1]
            elif data[0] == 'level':
                level = int(data[1])
            elif data[0] == 'points':
                points = int(data[1])
            elif data[0] == 'coordinates':
                coordinates = tuple(map(int, data[1].strip('() ').split(', ')))
                coordinate = coordinates[0], coordinates[1]
            elif data[0] == 'skin':
                skin = data[1]
            elif data[0] == 'game':
                num = int(data[1])

                if 'name' in locals() and level == game.level and coordinate != (0, 0):
                    students.append(Student(name=name, level=level, points=points, coordinates=coordinate, game=num, skin=skin))

    if len(students) < game.level:
        for i, row in enumerate(game.maze):
            for j, cell in enumerate(row):
                if cell == 's' and all((i, j) != student.coordinate for student in students):
                    students.append(Student(name='Student', level=game.level, points=0, coordinates=(i, j), game=len(students) + 1))

    return students


def set_students(game) -> list[Student]:
    """
    Adjusts the number of students to match the required count based on the game's level.

    Args:
        game: An object representing the current state of the game.

    Returns:
        A list of Student objects, adjusted to match the required count based on the game's level.
    """
    students = get_students(game)

    if len(students) < game.level // 2 or len(students) == 0:
        i = len(students)
        while True:
            num = len(students) + 1
            coord_x = choice(range(len(game.maze)))
            coord_y = choice(range(len(game.maze[0])))
            coordinate = (coord_x, coord_y)
            if coordinate == (len(game.maze), len(game.maze[-1])):
                continue
            students.append(Student(name='Student' + str(i + 1), level=game.level, points=0, coordinates=coordinate, game=num))
            i += 1
            if i >= game.level // 2:
                break
    elif len(students) > game.level // 2:
        students = sorted(students, key=lambda student: student.num, reverse=True)[:game.level // 2]

    return students


def get_history() -> list[Student]:
    """
    Reads a history file to retrieve and create a list of Student objects, then sorts them by their points in descending order.

    Returns:
    List[Student]: A sorted list of Student objects based on their points.
    """
    students: list[Student] = []

    # Getting history lines and checking if file is empty
    if path.exists(HISTORY) and path.getsize(HISTORY) > 0:
        with open(HISTORY, 'r') as file:
            lines = file.readlines()
        if len(lines) == 1 and lines[0].strip() == '':
            return []

        # Read and create Student objects from history file
        student_info = {}
        for line in lines:
            key, value = line.strip().split(': ', 1)
            student_info[key] = value.strip()
            if isinstance(student_info[key], str) and key == 'coordinates':
                student_info[key] = tuple(map(int, student_info[key].strip('() ').split(', ')))
            elif isinstance(student_info[key], str) and student_info[key].isnumeric():
                student_info[key] = int(student_info[key])
            if len(student_info) == 4:
                students.append(Student(**student_info))
                student_info = {}

    # Sorting students based in points
    students.sort(key=lambda x: x.points, reverse=True)

    return students
