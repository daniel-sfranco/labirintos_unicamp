import pygame
from pygame.font import Font
from player import *

size = width, height = 1200, 600
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption('Labirintos da Unicamp')
clock = pygame.time.Clock()

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

def draw_name():
    screen.fill('black')
    base_font = Font(None, 32)
    pygame.draw.rect(screen, '#FFFFFF', (width//2 - 300, height // 2 - 100, width//2 + 300, height//2 + 100))
def draw_maze(player, maze_object):
    wall = pygame.image.load("img/tiles/roomWall12.gif").convert()
    screen.fill('black')
    maze = maze_object.maze
    maze_width = maze_height = len(maze)
    unit_size = (3 * width // 4) // maze_width if width > height else (3 * height // 4) // maze_height
    player.img = pygame.transform.scale(player.img, (unit_size, unit_size))
    wall = pygame.transform.scale(wall, (unit_size, unit_size))
    player_y = player.coordinate[0] * unit_size
    player_x = player.coordinate[1] * unit_size
    if player_y > height//2:
        dif = player_y - height//2
        max = ((len(maze) - 1) * unit_size) - dif
        if max >= height - 2 * unit_size:
            maze_object.player_dif = dif
    else: maze_object.player_dif = 0
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[y][x] == 1:
                wall_y = y * unit_size - maze_object.player_dif
                wall_x = x * unit_size
                screen.blit(wall, (wall_x, wall_y))
    screen.blit(player.img, (player_x, player_y - maze_object.player_dif))
    return unit_size