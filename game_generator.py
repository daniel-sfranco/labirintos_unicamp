import random
from typing import Any, Union
import pygame


class GameGenerator:
    def __init__(self, level: int, profs:int = 3, maze: list[list[Any]] = [], time=60):
        self.level = level
        self.width = level + 6
        self.height = level + 6
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]  # Initialize grid as 0s
        self.player_dif = 0
        self.profs = profs
        self.time = time
        if maze == []:
            self.maze: list[list[Any]] = [[0 for _ in range(2 * self.width - 1)] for _ in range(2 * self.height - 1)]
            self.generate_maze()
        else:
            self.maze = maze
        self.start = pygame.time.get_ticks()
        self.stop = 0
        self.dif = 0

    def generate_maze(self):
        # Start at a random cell
        current_cell = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        closed = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i % 2 == 1 or j % 2 == 1:
                    self.maze[i][j] = 1
        # Recursively generate the maze starting from the current cell
        self.generate_maze_recursive(current_cell, closed)
        self.maze[0][0] = 'p'
        return self.maze

    def generate_maze_recursive(self, cell, closed):
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

    def get_unvisited_neighbors(self, cell):
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

    def remove_wall(self, cell1, cell2):
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

    def print_maze(self):
        for row in self.maze:
            print(" ".join(["#" if cell else " " for cell in row]))
        print()

    def reset(self, time):
        p_reset = False
        i = j = 0
        while i < len(self.maze) and not p_reset:
            while j < len(self.maze[i]) and not p_reset:
                if self.maze[i][j] == 'p':
                    self.maze[i][j] = 0
                    p_reset = True
                j += 1
            i += 1
        self.maze[0][0] = 'p'
        self.time = time
        self.start = pygame.time.get_ticks()
        self.dif = 0

if __name__ == "__main__":
    level = int(input('Level: '))

    # Create a maze generator instance and specify the maze dimensions
    maze_generator = GameGenerator(level, 0)

    # Print the maze representation
    maze_generator.print_maze()
