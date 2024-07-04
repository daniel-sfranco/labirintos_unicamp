from constants import *
import random
import audio
from typing import Any
import time
from player import Player
from student import set_students, get_students
from teacher import Teacher, set_teachers


class Game:
    def __init__(self, level: int, maze: list[list[Any]] = [], init_maze=[], act_time=TIME) -> None:
        """
        Initialize a Game object with given level, maze, initial maze state, and active time.

        Args:
            level (int): An integer representing the game level.
            maze (list[list[Any]]): A list of lists representing the maze structure (optional).
            init_maze (list[list[Any]]): A list of lists representing the initial maze state (optional).
            act_time (float): The active time for the game (optional, default is TIME).
        """
        self.level = level
        self.width = level + 6
        self.height = level + 6
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]  # Initialize grid as 0s
        self.player_dif = 0
        self.time = act_time
        self.time_dif = TIME - act_time
        self.points = 0
        self.act_points = 0
        self.num_students = level
        self.num_teachers = level
        self.end = False
        self.bomb_start: float = 0
        self.bomb_coords: tuple[int, int] = (-1, -1)
        self.bomb_time: float = -1

        # Set maze
        if not maze:
            self.maze: list[list[Any]] = [[0 for _ in range(2 * self.width - 1)] for _ in range(2 * self.height - 1)]
            self.generate_maze()
        else:
            self.maze = maze
            self.teachers = set_teachers(self)
            self.students = get_students(self)
            for teacher in self.teachers:
                self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'
            for student in self.students:
                self.maze[student.coordinate[0]][student.coordinate[1]] = 's'

        # Set init_maze to maze, except for students and teachers
        if not init_maze:
            self.init_maze = [[cell if cell not in ['s', 't'] else 0 for cell in row] for row in self.maze]
        else:
            self.init_maze = init_maze

        # Setting unit_size, used for plotting maze into screen
        maze_width = maze_height = len(self.maze)
        if WIDTH > HEIGHT:
            self.unit_size = (3 * WIDTH // 4) // maze_width + 1
        else:
            self.unit_size = (3 * HEIGHT // 4) // maze_height + 1

        self.start = time.perf_counter()

    def generate_maze(self) -> list[list[Any]]:

        #Set initial walls at all odd lines and columns
        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        current_cell = (current_x, current_y)
        closed = set()
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i % 2 == 1 or j % 2 == 1:
                    self.maze[i][j] = 1

        # Recursively generate the maze starting from the current cell
        self.generate_maze_recursive(current_cell, closed)

        # Defining player position at first position
        self.maze[0][0] = 'p'

        # Defining students' position and plotting in maze
        self.students = set_students(self)
        for student in self.students:
            self.maze[student.coordinate[0]][student.coordinate[1]] = 's'

        # Defining initial teachers' position and plotting in maze
        self.teachers: list[Teacher] = set_teachers(self)
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'

        # Plotting some points in maze
        i = 0
        while i < self.level + 6:
            random_x = random.randint(0, len(self.maze[0]) - 1)
            random_y = random.randint(0, len(self.maze) - 1)
            if self.maze[random_y][random_x] == 0:
                self.maze[random_y][random_x] = 'n'
                i += 1
        return self.maze

    def generate_maze_recursive(self, cell: tuple[int, int], closed: set[tuple[int, int]]) -> None:

        # Mark the current cell as visited
        self.grid[cell[0]][cell[1]] = 1
        closed.add(cell)

        # Get all unvisited neighbors and shuffling them
        neighbors = self.get_unvisited_neighbors(cell)
        random.shuffle(neighbors)

        # Explore each neighbor, removing walls between current cell and neighbor and calling itself again for each neighbor
        for next_cell in neighbors:
            wall = self.remove_wall(cell, next_cell)
            if next_cell not in closed:
                self.maze[wall[0]][wall[1]] = 0
            # Recursion call for each neighbor
            self.generate_maze_recursive(next_cell, closed)

    def get_unvisited_neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        neighbors = []
        x, y = cell

        # Check for valid neighbors and add them to the list if unvisited
        if x > 0 and self.grid[x - 1][y] == 0:
            neighbors.append((x - 1, y))  # Left neighbor
        if x < self.height - 1 and self.grid[x + 1][y] == 0:
            neighbors.append((x + 1, y))  # Right neighbor
        if y > 0 and self.grid[x][y - 1] == 0:
            neighbors.append((x, y - 1))  # Top neighbor
        if y < self.width - 1 and self.grid[x][y + 1] == 0:
            neighbors.append((x, y + 1))  # Bottom neighbor

        return neighbors

    def remove_wall(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> tuple[int, int]:
        x1, y1 = cell1
        x2, y2 = cell2

        # Determine the direction of the wall to remove
        if x1 == x2:
            # Vertical wall
            wall_y = min(y1, y2) + 1
            self.grid[x1][wall_y] = 1  # Mark the wall as removed
            return (x1 * 2, min(y1, y2) * 2 + 1)
        else:
            # Horizontal wall
            wall_x = min(x1, x2) + 1
            self.grid[wall_x][y1] = 1  # Mark the wall as removed
            return (min(x1, x2) * 2 + 1, y1 * 2)

    def reset(self) -> None:
        # Uploading maze to initial maze
        self.maze = [[self.init_maze[i][j] for j in range(len(self.init_maze[i]))] for i in range(len(self.init_maze))]

        # Setting teacher to their initial positions
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 0
        self.teachers = set_teachers(self)
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'

        # Setting students again to their positions
        self.students = set_students(self)
        for student in self.students:
            self.maze[student.coordinate[0]][student.coordinate[1]] = 's'

        # Resolving game time and actual points
        self.start = time.perf_counter()
        self.time_dif = 0
        self.time = TIME
        self.act_points = 0

    def detonate(self, player: Player, bomb_coords: tuple[int, int]) -> Player:
        """
        Simulates the detonation of a bomb in the game, affecting the surrounding area.
        Removes teachers within the blast radius, updates the maze, and checks if the player is within the blast radius to reset their state if necessary.
        An explosion sound is played at the end.

        Args:
            player (Player): An instance of the Player class representing the current player.
            bomb_coords (tuple[int, int]): A tuple of integers representing the coordinates where the bomb is detonated.

        Returns:
            Player: The updated Player instance after the detonation effects are applied.
        """
        for i in range(max(0, bomb_coords[0] - 1), min(len(self.maze), bomb_coords[0] + 2)):
            for j in range(max(0, bomb_coords[1] - 1), min(len(self.maze[i]), bomb_coords[1] + 2)):
                del_teachers = [t for t in self.teachers if t.coordinate == [i, j]]
                for t in del_teachers:
                    self.teachers.remove(t)
                self.maze[i][j] = 0

        if abs(bomb_coords[0] - player.coordinate[0]) < 2 and abs(bomb_coords[1] - player.coordinate[1]) < 2:
            self.reset()
            player.lives -= 1
            player.coordinate = (0, 0)
            player.points = player.first_points
            player.bombs = player.first_bomb

        audio.explosion.play()
        return player


if __name__ == "__main__":
    level = int(input('Level: '))
    # Create a maze generator instance and specify the maze dimensions
    game = Game(level)
    for i in game.maze:
        for j in i:
            print(str(j), end=' ')
        print()
