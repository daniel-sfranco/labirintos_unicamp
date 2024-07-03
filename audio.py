import pygame

explosion = pygame.mixer.Sound('./audio/explosion.wav')
points = pygame.mixer.Sound('./audio/points.wav')
points.set_volume(0.7)
select = pygame.mixer.Sound('./audio/select.wav')
select.set_volume(0.5)
wrong = pygame.mixer.Sound('./audio/wrong.wav')
correct = pygame.mixer.Sound('./audio/correct.wav')
level_complete = pygame.mixer.Sound('./audio/level_complete.wav')