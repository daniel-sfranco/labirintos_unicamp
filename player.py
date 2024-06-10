import pygame
from drawer import *

size = width, height = 900, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def create_player():
    player = pygame.image.load('img/player/human.gif')
    playerrect = player.get_rect()
    return player, playerrect

def move_player(key, playerrect):
    speed = 1
    full_speed = []
    if key in [pygame.K_DOWN, pygame.K_s] and playerrect.bottom <= height + 1:
        full_speed = [0, speed]
    elif key in[pygame.K_UP, pygame.K_w] and playerrect.top >= -1:
        full_speed = [0, speed * -1]
    elif key in [pygame.K_LEFT, pygame.K_a] and playerrect.left >= -1:
        full_speed = [speed * -1, 0]
    elif key in [pygame.K_RIGHT, pygame.K_d] and playerrect.right <= width + 1:
        full_speed = [speed, 0]
    else: full_speed = [0, 0]
    playerrect = playerrect.move(full_speed)
    pygame.time.delay(10)
    return playerrect