import pygame
import os
import audio
from constants import BOMBS, LIVES, MOVE_KEYS, SPEED


class Player:
    def __init__(self, name: str, skin: str = 'superhero', points: int = 0, lives: int = LIVES, bombs: int = BOMBS, coordinate: tuple[int, int] = (0, 0), level: int = 0) -> None:
        """
        Initialize a Player object with given attributes.

        Args:
            name (str): The name of the player.
            skin (str): The skin/appearance of the player.
            points (int): The current points of the player.
            lives (int): The current lives of the player.
            bombs (int): The current bombs the player has.
            coordinate (tuple[int, int]): The current position of the player in the maze.
            level (int): The current level of the player.
        """
        self.name = name
        self.points = points
        self.lives = lives
        self.bombs = bombs
        self.first_lives = lives
        self.first_bomb = bombs
        self.first_points = points
        self.coordinate = coordinate
        self.time_dif = 0
        self.skin = skin.strip()
        self.facing_right = True
        self.level = level
        self.img = pygame.image.load(f'img/player/{self.skin}.gif').convert()

    def move_player(self, game) -> tuple[int, int]:
        """
        Handle player movement based on key inputs and update the game state.

        Args:
            game: The game object where the player is moving.

        Returns:
            tuple[int, int]: The next coordinates of the player after movement.
        """
        maze = game.maze
        keys = pygame.key.get_pressed()
        y, x = self.coordinate
        actual_key = next((key for key in MOVE_KEYS if keys[key]), 0)

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

        first = maze[y][x]
        next_cell = maze[next_coordinate[0]][next_coordinate[1]]

        if first != next_cell and next_cell != 1:
            if first == 'p':
                first = 0
            else:
                first = ''.join([letter for letter in first if letter != 'p'])

            if next_cell == 0:
                next_cell = 'p'
            elif next_cell == 'n':
                next_cell = 'p'
                game.act_points += 1
                audio.points.play()
            elif next_cell == 'b':
                self.bombs += 1
                next_cell = 'p'
            elif next_cell in ['s', 't']:
                pygame.time.delay(SPEED)
                return next_coordinate
            elif next_cell == 'l':
                next_cell = 'p'
                self.lives += 1
            elif next_cell == 'c':
                self.time_dif += 15
                next_cell = 'p'
            else:
                return next_coordinate

            maze[y][x] = first
            pygame.time.delay(SPEED)
            maze[next_coordinate[0]][next_coordinate[1]] = next_cell
            self.coordinate = next_coordinate

        return next_coordinate
