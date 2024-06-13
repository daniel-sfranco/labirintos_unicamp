import pygame
from pygame.font import Font
import sys

size = width, height = 900, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Labirinto da Unicamp')
clock = pygame.time.Clock()

def draw_init():
    font = Font(None, 50)
    title = font.render('LABIRINTO DA UNICAMP', True, '#FFFFFF')
    titlerect = title.get_rect()
    titlerect.top = 50
    titlerect.centerx = width/2
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
    screen.blit(title, titlerect)
    pygame.display.flip()
    return button_positions
def draw_player(player, playerrect):
    screen.fill("black")
    screen.blit(player, playerrect)
    pygame.display.flip()
