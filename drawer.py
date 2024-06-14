import pygame
from pygame.font import Font
from player import *

size = width, height = 1300, 660
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Labirinto da Unicamp')
clock = pygame.time.Clock()
wall = pygame.image.load("img/tiles/roomWall12.gif").convert()
player = pygame.image.load('img/player/human.gif').convert()

def draw_init():
    font = Font(None, 50)
    title = font.render('LABIRINTOS DA UNICAMP', True, '#FFFFFF')
    title_rect = title.get_rect()
    title_rect.top = 50
    title_rect.centerx = width/2
    button_width = 400
    button_height = 50
    button_backgroundcolor = '#FFFFFF'
    button_textcolor = '#000000'
    button_x = (width - button_width)/2
    button_y = [150, 210, 270, 330, 390]
    button_text = ['Novo Jogo', 'Carregar Jogo', 'Exibir Ganhadores', 'Informações', 'Sair']
    button_positions = []
    font = Font(None, 24)
    for i in range(5):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height/2)))
        pygame.draw.rect(screen, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        screen.blit(text_surface, text_rect)
        button_positions.append((button_x, button_x + button_width, button_y[i], button_y[i] + button_height))
    screen.blit(title, title_rect)
    pygame.display.flip()
    return button_positions
def draw_player(player, player_rect):
    screen.blit(player, player_rect)

def draw_maze(maze_object):
    global player, wall, wall_list, move_keys
    screen.fill('black')
    maze = maze_object.maze
    maze_width = maze_height = len(maze)
    unit_size = width // maze_width if width < height else height // maze_height
    player = pygame.transform.scale(player, (unit_size, unit_size))
    wall = pygame.transform.scale(wall, (unit_size, unit_size))
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] == 1:
                wall_y = y * unit_size
                wall_x = x * unit_size
                screen.blit(wall, (wall_y, wall_x))
            elif maze[x][y] == 'p':
                player_y = y * unit_size
                player_x = x * unit_size
                screen.blit(player, (player_y, player_x))
    return unit_size