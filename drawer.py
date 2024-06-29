import pygame
from constants import *
from pygame.font import Font
from save import return_saves
from player import Player
from game_generator import GameGenerator

screen = SCREEN
pygame.display.set_caption('Labirintos da Unicamp')

def draw_init() -> list[pygame.Rect]:
    screen.fill(BLACK)
    title = titlefont.render('LABIRINTOS DA UNICAMP', True, '#FFFFFF')
    title_rect = title.get_rect()
    title_rect.top = HEIGHT//12
    title_rect.centerx = WIDTH//2
    button_x = (WIDTH - button_width)/2
    button_distance = HEIGHT//10
    button_y = [WIDTH//5 + i * button_distance for i in range(5)]
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
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
    if type == 'load':
        title = subfont.render('Escolha um jogo salvo', True, WHITE)
        pygame.draw.rect(surface, BLACK, [0, 0, WIDTH, HEIGHT])
    elif type == 'delete':
        draw_maze(player, game)
        title = subfont.render('Escolha um jogo para sobreescrever', True, WHITE)
        pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
    title_rect = title.get_rect()
    title_rect.top = HEIGHT//10
    title_rect.centerx = WIDTH//2
    surface.blit(title, title_rect)
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)

    games = return_saves()
    button_text = []
    for game in games:
        button_text.append(f'{game[2].name}: nível {game[1].level}, {game[2].lives} vidas')
    button_text.append('Limpar jogos salvos')
    button_text.append('Voltar')
    button_y = [WIDTH//6 + i * button_distance for i in range(len(button_text))]
    menu:list[pygame.Rect] = []
    for i in range(len(button_text)):
        text_surface = textfont.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_centerx + (button_width / 2), button_y[i] + (button_height/2)))
        rect = pygame.draw.rect(surface, button_backgroundcolor, (button_centerx, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)
        menu.append(rect)
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    return menu


def draw_pause_button():
    button_size = FIRST_UNIT // 4
    pause_img = pygame.transform.scale(pygame.image.load('img/x.jpeg').convert(), (button_size, button_size))
    pause_rect = pygame.Rect(WIDTH - 2 * button_size, button_size, button_size, button_size)
    screen.blit(pause_img, pause_rect)
    return pause_rect


def draw_name():
    screen.fill('black')
    # base_font = Font(None, 32)
    pygame.draw.rect(screen, WHITE, (WIDTH//2 - 300, HEIGHT // 2 - 100, WIDTH//2 + 300, HEIGHT//2 + 100))


def draw_maze(player, game_object):
    screen.fill(BLACK)
    maze_surface = pygame.Surface(SIZE)
    maze = game_object.maze
    maze_width = maze_height = len(maze)
    unit_size = (3 * WIDTH // 4) // maze_width + 1 if WIDTH > HEIGHT else (3 * HEIGHT // 4) // maze_height + 1
    player.img = pygame.transform.scale(player.img, (unit_size, unit_size))
    wall = pygame.transform.scale(WALL, (unit_size, unit_size))
    player_y = player.coordinate[0] * unit_size
    dif = 0
    max = len(maze) * unit_size
    while player_y > HEIGHT//2 and max > HEIGHT:
        dif += unit_size
        player_y -= unit_size
        max -= unit_size
    game_object.player_dif = dif
    for y in range(0, maze_height * unit_size, unit_size):
        for x in range(0, maze_width * unit_size,unit_size):
            maze_y = y//unit_size
            maze_x = x//unit_size
            if maze[maze_y][maze_x] == 1:
                maze_surface.blit(wall, (x, y - game_object.player_dif))
            elif maze[maze_y][maze_x] == 0: pass
            else:
                if 's' in maze[maze_y][maze_x]:
                    ghost = pygame.transform.scale(GHOST, (unit_size, unit_size))
                    maze_surface.blit(ghost, (x, y - game_object.player_dif))
                if 't' in maze[maze_y][maze_x]:
                    prof = pygame.transform.scale(PROF, (unit_size, unit_size))
                    maze_surface.blit(prof, (x, y - game_object.player_dif))
                if 'b' in maze[maze_y][maze_x]:
                    bomb = pygame.transform.scale(BOMB, (unit_size, unit_size))
                    maze_surface.blit(bomb, (x, y - game_object.player_dif))
    maze_surface.blit(player.img, (player.coordinate[1] * unit_size, player.coordinate[0] * unit_size - game_object.player_dif))
    screen.blit(maze_surface, (0, 0))
    return unit_size

def draw_HUD(game, player):
    lab = game.level
    points = player.points
    time = game.time
    life = player.lives
    bombs = player.bombs
    hud = pygame.Surface((SIZE), pygame.SRCALPHA)
    hud_height = HEIGHT//1.3
    hud_y = ((HEIGHT * 1.05) - hud_height)/2
    hud_width = WIDTH//4.5
    hud_x = (WIDTH - hud_width)/1.02
    pygame.draw.rect(hud, DARKGRAY, [hud_x, hud_y, hud_width, hud_height])

    text = ["Labirinto: " + str(lab), "Pontos: " + str(points), "Tempo: " + str(time),"S2: " + str(life), "Bombas: " + str(bombs)]
    font = Font(None, WIDTH//30)
    mini_size = FIRST_UNIT*0.35
    for i in range(len(text)):
        if i == 3:
            heart_size = (mini_size, mini_size)
            heart_icon = pygame.image.load('img/heart.png')
            heart_icon = pygame.transform.scale(heart_icon, heart_size)
            for j in range(life):
                heart_rect = pygame.Rect(hud_x + (hud_width / (i+1.8)) + j*mini_size, hud_y + (hud_height/(height_div/1)), mini_size, mini_size)
                hud.blit(heart_icon, heart_rect)
        elif i == 4:
            bomb_size = (mini_size, mini_size)
            bomb_icon = pygame.image.load('img/items/shortSword.gif')
            bomb_icon = pygame.transform.scale(bomb_icon, bomb_size)
            for j in range(bombs):
                bomb_rect = pygame.Rect(hud_x + (hud_width / (i+0.8)) + j*mini_size, hud_y + (hud_height/(height_div/1.2)), mini_size , mini_size)
                hud.blit(bomb_icon, bomb_rect)
        else:
            height_div = (5/(i+1))
            text_surface = font.render(text[i], True, WHITE)
            text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 2.2), hud_y + (hud_height/(height_div+0.3))))
            hud.blit(text_surface, text_rect)
    screen.blit(hud, (0,0))


def draw_pause_menu(player, game):
    draw_maze(player, game)
    draw_HUD(game, player)
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)

    title = subfont.render('Pausado', True, WHITE)
    title_rect = title.get_rect()
    title_rect.top = HEIGHT//10
    title_rect.centerx = WIDTH//2
    surface.blit(title, title_rect)

    button_distance = HEIGHT//10
    button_y = [WIDTH//6 + i * button_distance for i in range(5)]
    button_text = ['Voltar', 'Reiniciar labirinto atual', 'Salvar', 'Novo jogo', 'Sair']
    menu:list[pygame.Rect] = []
    for i in range(5):
        text_surface = textfont.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_centerx + (button_width / 2), button_y[i] + (button_height/2)))
        rect = pygame.draw.rect(surface, button_backgroundcolor, (button_centerx, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)
        menu.append(rect)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

    return menu

def draw_game_over(game,player):
   draw_maze(player, game)
   draw_HUD(game, player)
   surface = pygame.Surface((SIZE), pygame.SRCALPHA)
   pygame.draw.rect(surface, RED, [0, 0, WIDTH, HEIGHT])
   pygame.draw.rect(surface, BLACK, [menu_x, menu_y*1.3, menu_width, menu_height*0.7], 0, 20)

   title = subfont.render('FIM DE JOGO', True, WHITE)
   title_rect = title.get_rect()
   title_rect.top = HEIGHT//10
   title_rect.centerx = WIDTH//2
   surface.blit(title, title_rect)

   button_distance = HEIGHT//10
   button_y = [(WIDTH//6 + i * button_distance)*1.2 for i in range(3)]
   button_text = ['Novo jogo', 'Exibir ganhadores', 'Sair']
   menu:list[pygame.Rect] = []
   for i in range(3):
       text_surface = textfont.render(button_text[i], True, button_textcolor)
       text_rect = text_surface.get_rect(center=(button_centerx + (button_width / 2), button_y[i] + (button_height/2)))
       rect = pygame.draw.rect(surface, button_backgroundcolor, (button_centerx, button_y[i], button_width, button_height))
       surface.blit(text_surface, text_rect)
       menu.append(rect)
   screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

   return menu

def draw_character_sel(user_input):
    char_button_wi = button_width*0.3
    char_button_hei = button_height*0.6
    screen.fill(BLACK)
    title = titlefont.render('SELECIONE SEU PERSONAGEM', True, '#FFFFFF')
    title_rect = title.get_rect()
    title_rect.top = HEIGHT//12
    title_rect.centerx = WIDTH//2
    
    button_x = [WIDTH//8, WIDTH//1.3]
    button_y = HEIGHT//1.2

    font = Font(None, 24)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color(RED)
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    input_text = font.render(user_input, True, color)
    pygame.draw.rect(screen, color, input_box)
    screen.blit(input_text, input_box)

    button_text = ['Voltar', 'Concluir']
    button_positions = []
    for i in range(2):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x[i] + (char_button_wi / 2), button_y + (char_button_hei/2)))
        pygame.draw.rect(screen, button_backgroundcolor, (button_x[i], button_y, char_button_wi, char_button_hei))
        screen.blit(text_surface, text_rect)
        button_positions.append(pygame.Rect(button_x[i], button_y, char_button_wi, char_button_hei))
    screen.blit(title, title_rect)
    pygame.display.flip()
    return button_positions
