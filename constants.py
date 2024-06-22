import pygame
pygame.init()
INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
SCREEN=pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
TIME=60