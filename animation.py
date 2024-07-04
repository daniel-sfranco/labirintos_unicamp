import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self):
        self.sprites = []
        for i in range(3):
            self.sprites.append(pygame.image.load(f'img/items/bomb/bomb_ignited_{i + 1}.png'))
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()

    def update(self):
        self.current_sprite += 0.15

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        self.image = self.sprites[int(self.current_sprite)]