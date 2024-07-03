import pygame
pygame.init()
"""Índices matriz:
1 - muro
0 - espaço vazio
p - jogador
b - bomba
t - professor
s - estudante
A letra p pode se sobrepor a outras letras, tendo um tratamento diferente em cada caso.
"""
INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
TIME = 60
SPEED = 150
BOMB_TIME = 2
BOMBS = 0
LIVES = 3
SAVE = 'save.che'
HISTORY = 'history.che'
CHARACTERS = ['archer', 'barbarian', 'cleric', 'cyborg', 'ninja', 'paladin', 'superhero', 'thief']
FIRST_LEVEL = 1
FIRST_UNIT = (3 * WIDTH // 4) // (6 + FIRST_LEVEL) if WIDTH > HEIGHT else (3 * HEIGHT // 4) // (6 + FIRST_LEVEL)
CLOCK = pygame.time.Clock()
GHOST = pygame.image.load('img/player/ghost.gif').convert()
WALL = pygame.image.load("img/tiles/roomWall12.gif").convert()
PROF = pygame.image.load('img/player/scientist.gif').convert()
BOMB = pygame.image.load('img/items/bomb.png')
POINT = pygame.image.load('img/electricity.gif').convert()
HEART = pygame.image.load('img/heart.png')
CLOCK_ICON = pygame.image.load('img/items/clock.png')
TILE = pygame.image.load('img/darkness.gif')
GRAY = (128, 128, 128, 120)
DARKGRAY = '#282828'
LIGHTGRAY = '#575757'
GREEN = '#22C900'
DARKRED = '#EB0501'
BLUE = '#000022'
RED = (255, 0, 0, 120)
WHITE = '#FFFFFF'
BLACK = '#000000'
TILE_COLOR = '#0E0E0E'
BACKGROUND = BLACK
button_backgroundcolor = WHITE
button_textcolor = BLACK
button_width = WIDTH // 3
button_height = HEIGHT // 15
button_distance = HEIGHT // 10
button_centerx = (WIDTH - button_width) / 2
drawed_maze = False
game_part = 'init'
input_active = False
key_pressed = False
level = 1
menu_height = HEIGHT // 1.75
menu_y = ((HEIGHT * 1.05) - menu_height) / 2
menu_width = WIDTH // 2.5
menu_x = (WIDTH - menu_width) / 2
mouse_x, mouse_y = 0, 0
mouse_pressed = False
move_keys: list[int] = [
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_LEFT,
    pygame.K_a,
    pygame.K_s,
    pygame.K_w,
    pygame.K_d
]
questioned = False
screen = SCREEN
saved = False
skin_sel = 0
subfont = pygame.font.Font('./fonts/PixelTimes.ttf', WIDTH // 20)
textfont = pygame.font.Font('./fonts/PixelTimes.ttf', WIDTH // 60)
titlefont = pygame.font.Font('./fonts/dogicabold.ttf', WIDTH // 25)
user_input = ''
pygame.display.set_caption('Labirintos da Unicamp')
