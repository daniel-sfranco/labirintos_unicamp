import pygame
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]


class Player:
    def __init__(self, name: str, skin: int, points: int = 0, lives: int = 3, bombs: int = 0, coordinate: tuple[int, int] = (0,0)) -> None:
        self.name = name
        self.points = points
        self.lives = lives
        self.bombs = bombs
        self.coordinate = coordinate
        self.facing_right = True
        self.skin = skin
        if self.skin == 0:
            self.img = pygame.image.load('img/player/human.gif').convert()

    def move_player(self, maze_object):
        maze = maze_object.maze
        keys = pygame.key.get_pressed()
        coordinate: tuple[int, int] = (0,0)
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 'p':
                    coordinate = (y, x)
                    break
            if coordinate != (0,0) or maze[0][0] == 'p':
                break
        actual_key = 0
        for key in move_keys:
            if keys[key]:
                actual_key = key
                break
        if actual_key in [pygame.K_DOWN, pygame.K_s] and y < len(maze) - 1:
            next_coordinate = (y + 1, x)
        elif actual_key in [pygame.K_UP, pygame.K_w] and y > 0:
            next_coordinate = (y - 1, x)
        elif actual_key in [pygame.K_LEFT, pygame.K_a] and x > 0:
            next_coordinate = (y, x - 1)
            if self.facing_right:
                self.img = pygame.transform.flip(self.img, True, False)
                self.facing_right = False
        elif actual_key in [pygame.K_RIGHT, pygame.K_d] and x < len(maze[0]) - 1:
            next_coordinate = (y, x + 1)
            if not self.facing_right:
                self.img = pygame.transform.flip(self.img, True, False)
                self.facing_right = True
        else:
            next_coordinate = (y, x)
        if maze[next_coordinate[0]][next_coordinate[1]] != 1:
            maze[coordinate[0]][coordinate[1]] = 0
            maze[next_coordinate[0]][next_coordinate[1]] = 'p'
        else:
            next_coordinate = coordinate
        pygame.time.delay(125)
        if coordinate != next_coordinate:
            self.coordinate = next_coordinate

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            raise Exception('Game Over')