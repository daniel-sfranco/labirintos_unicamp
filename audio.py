import pygame

def music_setter(song):
    pygame.mixer.music.load(f'./audio/{song}.mp3')
    pygame.mixer.music.play(loops=-1)
    
# import sounds
explosion = pygame.mixer.Sound('./audio/explosion.wav')
points = pygame.mixer.Sound('./audio/points.wav')
select = pygame.mixer.Sound('./audio/select.wav')
wrong = pygame.mixer.Sound('./audio/wrong.wav')
correct = pygame.mixer.Sound('./audio/correct.wav')
level_complete = pygame.mixer.Sound('./audio/level_complete.wav')
choice = pygame.mixer.Sound('./audio/choice.wav')

#setting volumes
points.set_volume(0.7)
select.set_volume(0.5)
choice.set_volume(0.5)
pygame.mixer.music.set_volume(0.4)
