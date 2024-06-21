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

    def move_player(self, game):
        maze = game.maze
        keys = pygame.key.get_pressed()
        y, x = self.coordinate
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
        if maze[next_coordinate[0]][next_coordinate[1]] == 0:
            maze[self.coordinate[0]][self.coordinate[1]] = 0
            self.coordinate = next_coordinate
            pygame.time.delay(150)
        maze[self.coordinate[0]][self.coordinate[1]] = 'p'


    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            raise Exception('Game Over')