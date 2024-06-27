import pygame
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]


class Player:
    def __init__(self, name: str, skin: int = 0, points: int = 0, lives: int = 3, bombs: int = 0, coordinate: tuple[int, int] = (0,0), level: int = 0) -> None:
        self.name = name
        self.points = points
        self.lives = lives
        self.bombs = bombs
        self.coordinate = coordinate
        self.facing_right = True
        self.skin = skin
        self.level = level
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
        first = maze[self.coordinate[0]][self.coordinate[1]]
        next = maze[next_coordinate[0]][next_coordinate[1]]
        if first != next and next != 1:
            if first == 'p':
                first = 0
            else:
                letters = []
                for l in first:
                    letters.append(l)
                first = ''.join([letter for letter in letters if letter!= 'p'])
            if next == 0:
                next = 'p'
            elif next == 'b':
                next = 'p'
                self.bombs += 1
            elif next == 0:
                next_coordinate = self.coordinate
            else:
                return next
            maze[self.coordinate[0]][self.coordinate[1]] = first
            pygame.time.delay(150)
            maze[next_coordinate[0]][next_coordinate[1]] = next
            self.coordinate = next_coordinate