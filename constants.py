import pygame
pygame.init()

"""Matrix representation:

1 - wall
0 - free
p - player
b - bomb
t - teacher
s - student
ab - active bomb
n - points
l - life
c - clock

Except for player overlapping bomb, all spaces in matrix will have only one of those
"""
# width and height of screen, and game clock
CLOCK = pygame.time.Clock()
INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = INFO.current_w, INFO.current_h

# displaying screen and setting width, height and position of some components
BUTTON_DISTANCE = HEIGHT // 10
BUTTON_HEIGHT = HEIGHT // 15
BUTTON_WIDTH = WIDTH // 3
MENU_HEIGHT = HEIGHT // 1.75
MENU_WIDTH = WIDTH // 2.5
MENU_X = (WIDTH - MENU_WIDTH) / 2
MENU_Y = ((HEIGHT * 1.05) - MENU_HEIGHT) / 2
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)

#Setting window caption
pygame.display.set_caption('Labirintos da Unicamp')

# Setting contants for game mechanics
BOMB_TIME = 2
BOMBS = 5
CHARACTERS = ['archer', 'barbarian', 'cleric', 'cyborg', 'ninja', 'paladin', 'superhero', 'thief']
FIRST_LEVEL = 1
FIRST_UNIT = (3 * WIDTH // 4) // (6 + FIRST_LEVEL) if WIDTH > HEIGHT else (3 * HEIGHT // 4) // (6 + FIRST_LEVEL)
FPS = 50
HISTORY = 'history.che'
LIVES = 3
MOVE_KEYS: list[int] = [
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_LEFT,
    pygame.K_a,
    pygame.K_s,
    pygame.K_w,
    pygame.K_d
]
SAVE = 'save.che'
SPEED = 150
TIME = 60

# Setting maze assets
GHOST = pygame.image.load('img/player/ghost.gif').convert()
WALL = pygame.image.load("img/tiles/roomWall12.gif").convert()
FLOOR = pygame.image.load("img/tiles/floor.png").convert()
PROF = pygame.image.load('img/player/scientist.gif').convert()
BOMB = pygame.image.load('img/items/bomb.png')
POINT = pygame.image.load('img/electricity.gif').convert()
HEART = pygame.image.load('img/heart.png')
CLOCK_ICON = pygame.image.load('img/items/clock.png')
DOOR = pygame.image.load('img/tiles/openDoor13.gif')

# Style
COLORS = {
    'GRAY': (128, 128, 128, 120),
    'DARKGRAY': '#282828',
    'LIGHTGRAY': '#575757',
    'GREEN': '#22C900',
    'DARKRED': '#E40000',
    'RED': (255, 0, 0, 120),
    'WHITE': '#FFFFFF',
    'BLACK': '#000000',
    'YELLOW': '#FFFF00',
    'ORANGE': '#FF8000',
    'BROWN': '#964B00',
    'PINK': '#FFC0CB',
    'CYAN': '#00FFFF',
}
BACKGROUND = COLORS['BLACK']
BUTTON_BACKGROUNDCOLOR = COLORS['WHITE']
BUTTON_TEXTCOLOR = COLORS['BLACK']
FADED_COLOR = COLORS['GRAY']
HUD_COLOR = COLORS['DARKGRAY']
TITLE_COLOR = COLORS['CYAN']
SUBFONT = pygame.font.Font('./fonts/PixelTimes.ttf', 28)
TEXTFONT = pygame.font.Font('./fonts/PixelTimes.ttf', 24)
TITLEFONT = pygame.font.Font('./fonts/dogicabold.ttf', WIDTH // 25)
