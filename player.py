import pygame
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]


class Player:
    def __init__(self, name: str, skin: int) -> None:
        self.name = name
        self.points = 0
        self.lives = 3
        self.bombs = 0
        self.coordinate = (0, 0)
        self.facing_right = True
        self.skin = skin
        if self.skin == 0:
            self.img = pygame.image.load('img/player/human.gif').convert()

    def move_player(self, maze_object):
        maze = maze_object.maze
        keys = pygame.key.get_pressed()
        coordinate = ()
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 'p':
                    coordinate = (y, x)
                    break
            if coordinate:
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
