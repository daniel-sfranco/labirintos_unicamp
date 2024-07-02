import pygame
import os
from questions import ask_question
from constants import SPEED, BOMBS, LIVES, move_keys


class Player:
    def __init__(self, name: str, skin: str = 'human', points: int = 0, lives: int = LIVES, bombs: int = BOMBS, coordinate: tuple[int, int] = (0, 0), level: int = 0) -> None:
        self.name = name
        self.points = points
        self.lives = lives
        self.bombs = bombs
        self.first_lives = lives
        self.first_bomb = bombs
        self.first_points = points
        self.coordinate = coordinate
        self.time_dif = 0
        if '\n' in skin:
            self.skin = skin[:-1]
        else:
            self.skin = skin
        self.facing_right = True
        self.level = level
        path: str = os.path.join('img', 'player', f'{self.skin}.gif')
        self.img = pygame.image.load(path).convert()

    def move_player(self, game) -> tuple[int, int]:
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
        elif self.coordinate == (len(game.maze) - 1, len(game.maze) - 1) and actual_key in [pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN, pygame.K_s]:
            self.first_bomb = self.bombs
            self.first_lives = self.lives
            return (-1, -1)
        else:
            next_coordinate = (y, x)
        first = maze[self.coordinate[0]][self.coordinate[1]]
        next = maze[next_coordinate[0]][next_coordinate[1]]
        if first != next and next != 1:
            if first == 'p':
                first = 0
            else:
                letters = []
                for letter in first:
                    letters.append(letter)
                first = ''.join([letter for letter in letters if letter != 'p'])
            if next == 0:
                next = 'p'
            elif next == 'n':
                next = 'p'
                game.act_points += 1
            elif next == 'b':
                self.bombs += 1
                next = 'p'
            elif next == 's' or next == 't':
                pygame.time.delay(SPEED)
                return next_coordinate
            elif next == 'l':
                next = 'p'
                self.lives += 1
            elif next == 'c':
                self.time_dif += 15
                next = 'p'
            else:
                return next_coordinate
            maze[self.coordinate[0]][self.coordinate[1]] = first
            pygame.time.delay(SPEED)
            maze[next_coordinate[0]][next_coordinate[1]] = next
            self.coordinate = next_coordinate
        return next_coordinate
