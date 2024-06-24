import pygame
pygame.init()
INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
SCREEN=pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
TIME=60
GRAY = (128,128,128,120)
DARKGRAY = '#282828'
WHITE = '#FFFFFF'
BLACK = '#000000'
FIRST_LEVEL = 1
FIRST_UNIT = (3 * WIDTH // 4) // (6 + FIRST_LEVEL) if WIDTH > HEIGHT else (3 * HEIGHT // 4) // (6 + FIRST_LEVEL)
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