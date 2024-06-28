import pygame
pygame.init()
"""Índices matriz:
1 - muro
0 - espaço vazio
p - jogador
b - bomba
t - professor
g - fantasma
A letra p pode se sobrepor a outras letras, tendo um tratamento diferente em cada caso.
"""
INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
SCREEN=pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
TIME=60
SAVE='save.che'
HISTORY='history.che'
GRAY = (128,128,128,120)
DARKGRAY = '#282828'
RED = (255,0,0,120)
WHITE = '#FFFFFF'
BLACK = '#000000'
FIRST_LEVEL = 1
FIRST_UNIT = (3 * WIDTH // 4) // (6 + FIRST_LEVEL) if WIDTH > HEIGHT else (3 * HEIGHT // 4) // (6 + FIRST_LEVEL)
CLOCK = pygame.time.Clock()
GHOST = pygame.image.load('img/monsters/ghost.gif').convert()
WALL = pygame.image.load("img/tiles/roomWall12.gif").convert()
PROF = pygame.image.load('img/player/scientist.gif').convert()
BOMB = pygame.image.load('img/items/shortSword.gif').convert()
BOMB_TIME = 2
button_backgroundcolor = WHITE
button_textcolor = BLACK
button_width = WIDTH//3
button_height = HEIGHT//15
button_distance = HEIGHT//10
button_centerx = (WIDTH - button_width)/2
menu_height = HEIGHT//1.75
menu_y = ((HEIGHT * 1.05) - menu_height)/2
menu_width = WIDTH//2.5
menu_x = (WIDTH - menu_width)/2
titlefont = pygame.font.Font(None, WIDTH//15)
subfont = pygame.font.Font(None, WIDTH//20)
textfont = pygame.font.Font(None, WIDTH//60)