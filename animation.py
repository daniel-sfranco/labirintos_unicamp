import pygame

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

    def update(self):
        """
        Updates the animation by advancing to the next frame.
        """
        self.current_sprite += 0.15

        if self.current_sprite >= len(self.sprites):
            self.image =pygame.image.load('img/empty.gif')
        else:
            self.image = self.sprites[int(self.current_sprite)]