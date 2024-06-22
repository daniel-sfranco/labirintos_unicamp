import pygame
from pygame.font import Font
from save import return_saves
from player import Player
from game_generator import GameGenerator

pygame.init()

info = pygame.display.Info()
size = width, height = info.current_w, info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.update()
pygame.display.set_caption('Labirintos da Unicamp')
clock = pygame.time.Clock()

def draw_init() -> list[pygame.Rect]:
    font = Font(None, width//15)
    screen.fill('black')
    title = font.render('LABIRINTOS DA UNICAMP', True, '#FFFFFF')
    title_rect = title.get_rect()
    title_rect.top = height//12
    title_rect.centerx = width//2
    button_width = width//3
    button_height = height//15
    button_backgroundcolor = '#FFFFFF'
    button_textcolor = '#000000'
    button_x = (width - button_width)/2
    button_distance = height//10
    button_y = [width//5 + i * button_distance for i in range(5)]
    button_text = ['Novo Jogo', 'Carregar Jogo', 'Exibir Ganhadores', 'Informações', 'Sair']
    button_positions = []
    font = Font(None, 24)
    for i in range(5):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height/2)))
        pygame.draw.rect(screen, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        screen.blit(text_surface, text_rect)
        button_positions.append(pygame.Rect(button_x, button_y[i], button_width, button_height))
    screen.blit(title, title_rect)
    pygame.display.flip()
    return button_positions


def draw_select_save(type='load', player=Player('', 0), game=GameGenerator(1)):
    """
    This function draws a menu to select a saved game or to overwrite a game.

    Parameters:
    type (str): The type of menu to be drawn. It can be 'load' or 'delete'. Default is 'load'.
    player (Player): The player object. Default is an empty Player object.
    maze (GameGenerator): The maze object. Default is a GameGenerator object with level 1.

    Returns:
    list[pygame.Rect]: A list of pygame.Rect objects representing the positions of the menu buttons.
    """
    surface = pygame.Surface((size), pygame.SRCALPHA)
    pygame.draw.rect(surface, (128, 128, 128, 120), [0, 0, width, height])
    font = Font(None, width//19)
    if type == 'load':
        title = font.render('Escolha um jogo salvo', True, '#FFFFFF')
        pygame.draw.rect(surface, 'black', [0, 0, width, height])
    elif type == 'delete':
        draw_maze(player, game)
        title = font.render('Escolha um jogo para sobreescrever', True, '#FFFFFF')
        pygame.draw.rect(surface, (128, 128, 128, 120), [0, 0, width, height])
    title_rect = title.get_rect()
    title_rect.top = height//10
    title_rect.centerx = width//2
    surface.blit(title, title_rect)

    background_height = height//1.75
    background_y = ((height * 1.05) - background_height)/2
    background_width = width//2.5
    background_x = (width - background_width)/2
    pygame.draw.rect(surface, 'black', [background_x, background_y, background_width, background_height], 0, 20)

    button_width = width//3
    button_height = height//15
    button_backgroundcolor = '#FFFFFF'
    button_textcolor = '#000000'
    games = return_saves()
    button_text = []
    for game in games:
        button_text.append(f'Jogo {game[0]}: nível {game[1].level}, {game[2].lives} vidas')
    button_text.append('Limpar jogos salvos')
    button_text.append('Voltar')
    button_x = (width - button_width)/2
    button_distance = height//10
    button_y = [width//6 + i * button_distance for i in range(len(button_text))]
    font = Font(None, 24)
    menu:list[pygame.Rect] = []
    for i in range(len(button_text)):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height/2)))
        rect = pygame.draw.rect(surface, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)
        menu.append(rect)
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    return menu


def draw_pause_button(unit_size):
    pause_img = pygame.image.load('img/x.jpeg').convert()
    pause_img = pygame.transform.scale(pause_img, (unit_size // 2, unit_size // 2))
    pause_rect = pygame.Rect(width - 2 * unit_size // 2, unit_size // 2, unit_size // 2, unit_size // 2)
    screen.blit(pause_img, pause_rect)
    return pause_rect


def draw_name():
    screen.fill('black')
    # base_font = Font(None, 32)
    pygame.draw.rect(screen, '#FFFFFF', (width//2 - 300, height // 2 - 100, width//2 + 300, height//2 + 100))


def draw_maze(player, game_object):
    screen.fill('black')
    wall = pygame.image.load("img/tiles/roomWall12.gif").convert()
    maze = game_object.maze
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
            game_object.player_dif = dif
    else:
        game_object.player_dif = 0
    for x in range(maze_width):
        for y in range(maze_height):
            if maze[y][x] == 1:
                wall_y = y * unit_size - game_object.player_dif
                wall_x = x * unit_size
                screen.blit(wall, (wall_x, wall_y))
    screen.blit(player.img, (player_x, player_y - game_object.player_dif))
    return unit_size

def draw_HUD(lab = 1, life = 3, bombs = 3, points = 0, unit = 1, time = 0):
    hud = pygame.Surface((size), pygame.SRCALPHA)
    hud_height = height//1.3
    hud_y = ((height * 1.05) - hud_height)/2
    hud_width = width//4.5
    hud_x = (width - hud_width)/1.02
    pygame.draw.rect(hud, (40,40,40), [hud_x, hud_y, hud_width, hud_height])
    screen.blit(hud, (0,0))

    text = ["Labirinto: " + str(lab), "Pontos: " + str(points), "Tempo: " + str(time),"S2: " + str(life), "Bombas: " + str(bombs)]
    font = Font(None, width//30)
    mini_size = unit*0.7
    for i in range(len(text)):
        if i == 3:
            for j in range(life):
                hert_size = (unit*0.7, unit*0.7)
                heart_icon = pygame.image.load('img/heart.png')
                heart_icon = pygame.transform.scale(heart_icon, hert_size)
                heart_rect = pygame.Rect(hud_x + (hud_width / (i+1.8)) + j*mini_size, hud_y + (hud_height/(height_div/1)), mini_size, mini_size)
                screen.blit(heart_icon, heart_rect)
        elif i == 4:
            for j in range(bombs):
                bomb_size = (unit*0.7, unit*0.7)
                bomb_icon = pygame.image.load('img/items/bomb.png')
                bomb_icon = pygame.transform.scale(bomb_icon, bomb_size)
                heart_rect = pygame.Rect(hud_x + (hud_width / (i+0.8)) + j*mini_size, hud_y + (hud_height/(height_div/1.2)), mini_size , mini_size)
                screen.blit(bomb_icon, heart_rect)
        else:
            height_div = (5/(i+1))
            text_surface = font.render(text[i], True, '#FFFFFF')
            text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 2.2), hud_y + (hud_height/(height_div+0.3))))
            screen.blit(text_surface, text_rect)


def draw_pause_menu(player, game):
    draw_maze(player, game)
    draw_HUD(lab = game.level, time = game.time, life = player.lives)
    surface = pygame.Surface((size), pygame.SRCALPHA)
    pygame.draw.rect(surface, (128, 128, 128, 120), [0, 0, width, height])
    background_height = height//1.75
    background_y = ((height * 1.05) - background_height)/2
    background_width = width//2.5
    background_x = (width - background_width)/2
    pygame.draw.rect(surface, 'black', [background_x, background_y, background_width, background_height], 0, 20)

    font = Font(None, width//19)
    title = font.render('Pausado', True, '#FFFFFF')
    title_rect = title.get_rect()
    title_rect.top = height//10
    title_rect.centerx = width//2
    surface.blit(title, title_rect)

    button_width = width//3
    button_height = height//15
    button_backgroundcolor = '#FFFFFF'
    button_textcolor = '#000000'
    button_x = (width - button_width)/2
    button_distance = height//10
    button_y = [width//6 + i * button_distance for i in range(5)]
    button_text = ['Voltar', 'Reiniciar labirinto atual', 'Salvar', 'Novo jogo', 'Sair']
    font = Font(None, 24)
    menu:list[pygame.Rect] = []
    for i in range(5):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height/2)))
        rect = pygame.draw.rect(surface, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)
        menu.append(rect)
    screen.blit(surface, (0, 0, width, height), (0, 0, width, height))

    return menu
