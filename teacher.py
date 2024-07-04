from random import randint
from pygame import time
from player import Player
from constants import SPEED


class Teacher:
    def __init__(self, game, first_coordinate: tuple[int, int] = (-1, -1), coordinate: tuple[int, int] = (-1, -1)) -> None:
        """
        Initialize the Teacher object with a random position in the maze if not provided.

        Args:
            game: The game object.
            first_coordinate: The initial position of the teacher.
            coordinate: The current position of the teacher.
        """
        if first_coordinate == (-1, -1) and coordinate == (-1, -1):
            while True:
                x = randint(0, len(game.maze) - 1)
                y = randint(0, len(game.maze[0]) - 1)
                if (x, y) != (len(game.maze) - 1, len(game.maze[0]) - 1) and game.maze[x][y] == 0:
                    self.coordinate: tuple[int, int] = (x, y)
                    self.first_coordinate: tuple[int, int] = self.coordinate
                    break
        else:
            self.coordinate: tuple[int, int] = coordinate
            self.first_coordinate: tuple[int, int] = first_coordinate

    def move(self, player: Player, game, move=False):
        """
        Move the teacher towards the player if possible, updating the maze accordingly.

        Args:
            player: The player object.
            game: The game object.
            move: A flag indicating if the teacher should move.

        Returns:
            Updated maze after moving the teacher.
        """
        if move:
            speed = 0
        else:
            speed = SPEED // len(game.teachers)

        next_coord: tuple[int, int] = (-1, -1)
        if self.coordinate[0] == player.coordinate[0]:
            if self.coordinate[1] > player.coordinate[1]:
                next_coord = (self.coordinate[0], self.coordinate[1] - 1)
            elif self.coordinate[1] < player.coordinate[1]:
                next_coord = (self.coordinate[0], self.coordinate[1] + 1)
        elif self.coordinate[1] == player.coordinate[1]:
            if self.coordinate[0] > player.coordinate[0]:
                next_coord = (self.coordinate[0] - 1, self.coordinate[1])
            elif self.coordinate[0] < player.coordinate[0]:
                next_coord = (self.coordinate[0] + 1, self.coordinate[1])

        if next_coord != (-1, -1) and game.maze[next_coord[0]][next_coord[1]] == 0:
            game.maze[self.coordinate[0]][self.coordinate[1]] = 0
            game.maze[next_coord[0]][next_coord[1]] = 't'
            self.coordinate = next_coord

        time.delay(speed)
        return game.maze


def set_teachers(game) -> list[Teacher]:
    """
    Initializes and returns a list of Teacher objects based on the current state of the game maze.
    It either places teachers at predefined positions marked by 't' in the maze or randomly generates new positions if none are predefined.

    Args:
    - game: The game object containing the maze and other game-related attributes.

    Returns:
    - A list of Teacher objects placed in the maze.
    """
    teachers = []
    teacher_pos = [(y, x) for y in range(len(game.maze)) for x in range(len(game.maze[y])) if game.maze[y][x] == 't']

    if teacher_pos:
        teachers = [Teacher(game, first_coordinate=pos, coordinate=pos) for pos in teacher_pos]
    else:
        for _ in range(game.level // 2):
            teachers.append(Teacher(game))

    return teachers
