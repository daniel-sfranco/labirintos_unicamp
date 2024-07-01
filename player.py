import pygame
from questions import ask_question
from constants import SPEED, BOMBS, LIVES, TIME
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]
import os
import sys

class Player:
    def __init__(self, name: str, skin: str = 'human', points: int = 0, lives: int = LIVES, bombs: int = BOMBS, coordinate: tuple[int, int] = (0,0), level: int = 0) -> None:
        self.name = name
        self.points = points
        self.lives = lives
        self.bombs = bombs
        self.coordinate = coordinate
        if '\n' in skin:
            self.skin = skin[:-1]
        else:
            self.skin = skin
        self.facing_right = True
        self.level = level
        path: str = os.path.join('img', 'player', f'{self.skin}.gif')
        self.img = pygame.image.load(path).convert()

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
            if self.coordinate == (len(game.maze) - 1, len(game.maze) - 1):
                return True
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
            return True
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
            elif next == 'n':
                next = 'p'
                game.act_points += 1
            elif next == 'b':
                self.bombs += 1
                next = 'p'
            elif next == 's' or next == 't':
                question = ask_question()
                print(question)
                pygame.time.delay(SPEED)
                return False
            else:
                return False
            maze[self.coordinate[0]][self.coordinate[1]] = first
            pygame.time.delay(SPEED)
            maze[next_coordinate[0]][next_coordinate[1]] = next
            self.coordinate = next_coordinate
        return False