from constants import *
import random
from typing import Any
import time
from player import Player
from student import set_students, get_students
from teacher import Teacher, set_teachers


class Game:
    def __init__(self, level: int, maze: list[list[Any]] = [], first_maze=[], act_time=TIME) -> None:
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
        if maze == []:
            self.maze: list[list[Any]] = [[0 for _ in range(2 * self.width - 1)] for _ in range(2 * self.height - 1)]
            self.generate_maze()
        else:
            self.maze = maze
            self.teachers = set_teachers(self)
            self.students = get_students(self)
            for teacher in self.teachers:
                self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'
            for student in self.students:
                self.maze[student.coordinate[0]][student.coordinate[1]] ='s'
            i = 0
        if first_maze == []:
            self.first_maze = []
            for i in range(len(self.maze)):
                self.first_maze.append([])
                for j in range(len(self.maze[i])):
                    if self.maze[i][j] not in ['s', 't']:
                        self.first_maze[i].append(self.maze[i][j])
                    else:
                        self.first_maze[i].append(0)
        else:
            self.first_maze = first_maze
        self.start = time.perf_counter()

    def generate_maze(self) -> list[list[Any]]:
        # Start at a random cell
        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        current_cell = (current_x, current_y)
        closed = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i % 2 == 1 or j % 2 == 1:
                    self.maze[i][j] = 1
        # Recursively generate the maze starting from the current cell
        self.generate_maze_recursive(current_cell, closed)
        self.maze[0][0] = 'p'
        self.students = set_students(self)
        for student in self.students:
            self.maze[student.coordinate[0]][student.coordinate[1]] = 's'
        self.teachers: list[Teacher] = set_teachers(self)
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'
        i = 0
        while i < self.level + 6:
            random_x = random.randint(0, len(self.maze[0]) - 1)
            random_y = random.randint(0, len(self.maze) - 1)
            if self.maze[random_y][random_x] == 0:
                self.maze[random_y][random_x] = 'n'
                i += 1
        return self.maze

    def generate_maze_recursive(self, cell: tuple[int, int], closed: list[tuple[int, int]]) -> None:
        # Mark the current cell as visited
        self.grid[cell[0]][cell[1]] = 1

        closed.append(cell)

        # Get all unvisited neighbors
        neighbors = self.get_unvisited_neighbors(cell)

        # Randomly shuffle the neighbors
        random.shuffle(neighbors)

        # Recursively explore each neighbor
        for next_cell in neighbors:
            # Remove the wall between the current cell and the neighbor
            wall = self.remove_wall(cell, next_cell)

            # Remove the wall between the current cell and the neighbor
            if next_cell not in closed:
                self.maze[wall[0]][wall[1]] = 0

            # Recursively generate the maze from the neighbor cell
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
        self.maze = []
        for i in range(len(self.first_maze)):
            self.maze.append([])
            for j in range(len(self.first_maze[i])):
                self.maze[i].append(self.first_maze[i][j])
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 0
        self.teachers = set_teachers(self)
        for teacher in self.teachers:
            self.maze[teacher.coordinate[0]][teacher.coordinate[1]] = 't'
        self.students = set_students(self)
        for student in self.students:
            self.maze[student.coordinate[0]][student.coordinate[1]] = 's'
        self.start = time.perf_counter()
        self.time_dif = 0
        self.time = TIME

    def detonate(self, player: Player, bomb_coords: tuple[int, int]) -> Player:
        for i in range(bomb_coords[0] - 1, bomb_coords[0] + 2):
            for j in range(bomb_coords[1] - 1, bomb_coords[1] + 2):
                if i >= 0 and i < len(self.maze) and j >= 0 and j < len(self.maze[i]):
                    del_teachers = []
                    for t in self.teachers:
                        if t.coordinate == [i, j]:
                            del_teachers.append(t)
                    for t in range(len(del_teachers)):
                        self.teachers.remove(del_teachers[t])
                    self.maze[i][j] = 0
        if abs(bomb_coords[0] - player.coordinate[0]) < 2 and abs(bomb_coords[1] - player.coordinate[1]) < 2:
            player.lives -= 1
            player.coordinate = (0, 0)
            self.reset()
            player.points = player.first_points
            player.lives = player.first_lives
            player.bombs = player.first_bomb
        return player


if __name__ == "__main__":
    level = int(input('Level: '))

    # Create a maze generator instance and specify the maze dimensions
    maze_generator = Game(level)
