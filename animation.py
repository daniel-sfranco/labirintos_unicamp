import pygame
from game_generator import Game

class Animation(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initializes the Animation sprite.
        Loads images for animation and sets initial state.
        """
        super().__init__()
        self.sprites: list[pygame.Surface] = [pygame.image.load(f'img/items/bomb/bomb_ignited_{i + 1}.png') for i in range(3)]
        self.current_sprite: float = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()

    def update(self, game: Game):
        """
        Updates the animation by advancing to the next frame.
        """
        
        if game.bomb_animation_time > 1.6:
            self.current_sprite = 0
        if game.bomb_animation_time <= 1.6 and game.bomb_animation_time > 0.7:
            self.current_sprite = 1
        elif game.bomb_animation_time <= 0.7:
            self.current_sprite = 2
    
        self.image = self.sprites[self.current_sprite]