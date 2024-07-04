import pygame

# import sounds
explosion = pygame.mixer.Sound('./audio/explosion.wav')
points = pygame.mixer.Sound('./audio/points.wav')
select = pygame.mixer.Sound('./audio/select.wav')
wrong = pygame.mixer.Sound('./audio/wrong.wav')
correct = pygame.mixer.Sound('./audio/correct.wav')
level_complete = pygame.mixer.Sound('./audio/level_complete.wav')
choice = pygame.mixer.Sound('./audio/choice.wav')

#setting some volumes
points.set_volume(0.7)
select.set_volume(0.5)
choice.set_volume(0.5)
