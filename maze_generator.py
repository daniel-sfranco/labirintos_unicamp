import random
class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]  # Initialize grid as 0s
        self.maze = [[0 for _ in range(2 * width - 1)] for _ in range(2 * height - 1)]
        self.removed_walls = []
        self.generate_maze()

    def generate_maze(self):
        # Start at a random cell
        current_cell = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        closed = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i % 2 == 1 or j % 2 == 1: self.maze[i][j] = 1
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

            # Push the removed wall onto the stack
            self.removed_walls.append(wall)
            
            # Remove the wall between the current cell and the neighbor
            if next_cell not in closed:
                self.maze[wall[0]][wall[1]] = 0

            # Recursively generate the maze from the neighbor cell
            self.generate_maze_recursive(next_cell, closed)

            # Backtrack by popping the removed wall from the stack
            self.removed_walls.pop()

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

if __name__ == "__main__":
    width = int(input('Width: '))
    height = int(input('Height: '))
    
    # Create a maze generator instance and specify the maze dimensions
    maze_generator = MazeGenerator(width, height)

    # Print the maze representation
    maze_generator.print_maze()
