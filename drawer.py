import pygame
from constants import *
from pygame.font import Font
from questions import Question
from save import return_saves
import audio
from player import Player
from game_generator import Game


def draw_init() -> list[pygame.Rect]:
    screen.fill(BLACK)
    draw_title('LABIRINTOS DA UNICAMP', titlefont, WHITE)
    button_text = ['Novo Jogo', 'Carregar Jogo', 'Exibir Ganhadores', 'Informações', 'Sair']
    button_positions: list[pygame.Rect] = draw_menu(button_text, 3)
    pygame.display.flip()
    return button_positions


def draw_menu(button_text: list[str], div: float, surface: pygame.Surface=SCREEN) -> list[pygame.Rect]:
    num_buttons = len(button_text)
    button_x = (WIDTH - button_width) / 2
    button_y = [round(HEIGHT / div) + i * button_distance for i in range(num_buttons)]
    button_positions: list[pygame.Rect] = []
    for i in range(num_buttons):
        text_surface = textfont.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height / 2)))
        pygame.draw.rect(surface, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)
        button_positions.append(pygame.Rect(button_x, button_y[i], button_width, button_height))
    return button_positions


def draw_title(text: str, font: Font, color, surface: pygame.Surface = SCREEN, back=BLACK, question=0):
    title = font.render(text, True, color)
    title_rect = title.get_rect()
    match question:
        case 0:
            title_rect.top = HEIGHT // 10
        case 1:
            title_rect.top = HEIGHT // 5
        case 2:
            title_rect.top = round(HEIGHT / 3.5)
    title_rect.centerx = WIDTH // 2
    surface.blit(title, title_rect)


def draw_select_save(type: str='load', player: Player=Player(''), game: Game=Game(1)) -> list[pygame.Rect]:
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
        pygame.draw.rect(surface, BLACK, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo salvo', subfont, WHITE, surface)
    elif type == 'delete':
        draw_maze(player, game)
        pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo para sobreescrever', subfont, WHITE, surface)
        pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)
    games = return_saves()
    button_text = []
    for save in games:
        button_text.append(f'{save[2].name}: nível {save[1].level}, {save[2].lives} vidas')
    button_text.append('Limpar jogos salvos')
    button_text.append('Voltar')
    menu: list[pygame.Rect] = draw_menu(button_text, 4, surface)
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    return menu


def draw_pause_button() -> pygame.Rect:
    button_size = FIRST_UNIT // 4
    pause_img = pygame.transform.scale(pygame.image.load('img/x.jpeg').convert(), (button_size, button_size))
    pause_rect = pygame.Rect(WIDTH - 2 * button_size, button_size, button_size, button_size)
    screen.blit(pause_img, pause_rect)
    return pause_rect


def draw_maze(player, game_object) -> int:
    screen.fill(BLACK)
    maze_surface = pygame.Surface(SIZE)
    maze = game_object.maze
    maze_width = maze_height = len(maze)
    unit_size = (3 * WIDTH // 4) // maze_width + 1 if WIDTH > HEIGHT else (3 * HEIGHT // 4) // maze_height + 1
    player.img = pygame.transform.scale(player.img, (unit_size, unit_size))
    player_y = player.coordinate[0] * unit_size
    dif = 0
    max = len(maze) * unit_size
    while player_y > HEIGHT // 2 and max > HEIGHT:
        dif += unit_size
        player_y -= unit_size
        max -= unit_size
    game_object.player_dif = dif
    wall = pygame.transform.scale(WALL, (unit_size, unit_size))
    tile = pygame.transform.scale(TILE, (unit_size, unit_size))
    ghost = pygame.transform.scale(GHOST, (unit_size, unit_size))
    prof = pygame.transform.scale(PROF, (unit_size, unit_size))
    bomb = pygame.transform.scale(BOMB, (unit_size, unit_size))
    point = pygame.transform.scale(POINT, (unit_size // 2, unit_size // 2))
    life = pygame.transform.scale(HEART, (unit_size, unit_size))
    clock = pygame.transform.scale(CLOCK_ICON, (unit_size, unit_size))
    for y in range(0, maze_height * unit_size, unit_size):
        for x in range(0, maze_width * unit_size, unit_size):
            maze_y = y // unit_size
            maze_x = x // unit_size
            if maze[maze_y][maze_x] == 1:
                maze_surface.blit(wall, (x, y - game_object.player_dif))
            else:
                maze_surface.blit(tile, (x, y - game_object.player_dif))
                if isinstance(maze[maze_y][maze_x], str):
                    if 's' in maze[maze_y][maze_x]:
                        maze_surface.blit(ghost, (x, y - game_object.player_dif))
                    if 't' in maze[maze_y][maze_x]:
                        maze_surface.blit(prof, (x, y - game_object.player_dif))
                    if 'b' in maze[maze_y][maze_x]:
                        maze_surface.blit(bomb, (x, y - game_object.player_dif))
                    if 'n' in maze[maze_y][maze_x]:
                        maze_surface.blit(point, (x + unit_size // 4, y - game_object.player_dif + unit_size // 4))
                    if 'l' in maze[maze_y][maze_x]:
                        maze_surface.blit(life, (x, y - game_object.player_dif))
                    if 'c' in maze[maze_y][maze_x]:
                        maze_surface.blit(clock, (x, y - game_object.player_dif))
    maze_surface.blit(player.img, (player.coordinate[1] * unit_size, player.coordinate[0] * unit_size - game_object.player_dif))
    screen.blit(maze_surface, (0, 0))
    return unit_size


def draw_HUD(game, player) -> None:
    lab = game.level
    actual_points = game.points
    total_points = player.points
    time = game.time
    life = player.lives
    bombs = player.bombs
    hud = pygame.Surface((SIZE), pygame.SRCALPHA)
    hud_height = HEIGHT // 1.3
    hud_y = ((HEIGHT * 1.05) - hud_height) / 2
    hud_width = WIDTH // 4.5
    hud_x = (WIDTH - hud_width) / 1.02
    pygame.draw.rect(hud, DARKGRAY, [hud_x, hud_y, hud_width, hud_height])

    text = [f"Labirinto: {lab}", f"Pontos: {actual_points}", f"Total: {total_points}", f"Tempo: {time}", f"S2: {life}", f"Bombas: {bombs}"]
    font = Font(None, WIDTH // 30)
    mini_size = FIRST_UNIT * 0.35
    for i in range(len(text)):
        if i == 4:
            heart_size = (mini_size, mini_size)
            heart_icon = pygame.transform.scale(HEART, heart_size)
            for j in range(life):
                heart_rect = pygame.Rect(hud_x + (hud_width / (i + 1.8)) + j * mini_size, hud_y + (hud_height / height_div), mini_size, mini_size)
                hud.blit(heart_icon, heart_rect)
        elif i == 5:
            bomb_size = (mini_size, mini_size)
            bomb_icon = pygame.transform.scale(BOMB, bomb_size)
            for j in range(bombs):
                bomb_rect = pygame.Rect(hud_x + (hud_width / (i + 0.8)) + j * mini_size, hud_y + (hud_height / (height_div / 1.2)), mini_size, mini_size)
                hud.blit(bomb_icon, bomb_rect)
        else:
            height_div = (6 / (i + 1))
            text_surface = font.render(text[i], True, WHITE)
            text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 2.2), hud_y + (hud_height / (height_div + 0.3))))
            hud.blit(text_surface, text_rect)
    screen.blit(hud, (0, 0))


def draw_pause_menu(player, game) -> list[pygame.Rect]:
    draw_maze(player, game)
    draw_HUD(game, player)
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)
    button_text = ['Voltar', 'Reiniciar labirinto atual', 'Salvar', 'Novo jogo', 'Sair']
    draw_title('Pausado', subfont, WHITE, surface=surface)
    menu = draw_menu(button_text, 3.5, surface)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))
    return menu


def draw_game_over(game, player) -> list[pygame.Rect]:
    draw_maze(player, game)
    draw_HUD(game, player)
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, RED, [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y * 1.3, menu_width, menu_height * 0.7], 0, 20)
    button_text = ['Novo jogo', 'Exibir ganhadores', 'Sair']
    draw_title('FIM DE JOGO', subfont, WHITE, surface)
    menu = draw_menu(button_text, 6, surface)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))
    return menu


def draw_character_sel(user_input, input_active, skin_sel) -> tuple[list[pygame.Rect], list[pygame.Rect], pygame.Rect, str]:
    char_button_w = button_width * 0.3
    char_button_h = button_height * 0.6
    screen.fill(BLACK)
    draw_title('SELECIONE SEU PERSONAGEM', titlefont, WHITE)

    button_x = [WIDTH // 8, WIDTH // 1.3]
    button_y = HEIGHT // 1.2

    font = Font(None, 24)
    input_box = pygame.Rect(WIDTH / 3, button_y, WIDTH // 3, button_height * 0.6)
    color_inactive = pygame.Color(LIGHTGRAY)
    color_active = pygame.Color(WHITE)
    if input_active:
        color = color_active
    else:
        color = color_inactive
    if user_input == "":
        input_text = font.render("Escolha o nome do seu personagem", True, BLACK)
    else:
        input_text = font.render(user_input, True, BLACK)
    input_rect = input_text.get_rect(center=(input_box.centerx, input_box.centery))
    pygame.draw.rect(screen, color, input_box)
    screen.blit(input_text, input_rect)
    button_text = ['Voltar', 'Concluir']
    button_positions: list[pygame.Rect] = []
    for i in range(2):
        text_surface = font.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x[i] + (char_button_w / 2), button_y + (char_button_h / 2)))
        pygame.draw.rect(screen, button_backgroundcolor, (button_x[i], button_y, char_button_w, char_button_h))
        screen.blit(text_surface, text_rect)
        button_positions.append(pygame.Rect(button_x[i], button_y, char_button_w, char_button_h))

    slide_y = HEIGHT // 4
    character_w = FIRST_UNIT // 0.5
    character_h = FIRST_UNIT // 0.4
    character_distance = 600
    for i in range(len(CHARACTERS)):
        slide_x = (WIDTH // 2.5 - (character_distance * skin_sel)) + i * character_distance
        if i == skin_sel:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + CHARACTERS[i] + '.gif'), (11, 11))
        else:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + CHARACTERS[i] + '.gif').convert_alpha(), (8, 8))
            darken_surface = pygame.Surface(character_img.get_size()).convert_alpha()
            darken_surface.fill((255, 255, 255, 150))
            character_img.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        character_rect = pygame.Rect(slide_x, slide_y, character_w, character_h)
        screen.blit(character_img, character_rect)

    skin_choice: str = CHARACTERS[skin_sel]

    arrow_w = FIRST_UNIT // 4
    arrow_h = FIRST_UNIT // 2
    arrow_left_img = pygame.transform.scale(pygame.image.load('img/arrowLeft.png'), (arrow_w, arrow_h))
    arrow_left_rect = pygame.Rect(WIDTH // 12, HEIGHT // 2.3, arrow_w, arrow_h)
    screen.blit(arrow_left_img, arrow_left_rect)
    arrow_right_img = pygame.transform.flip(arrow_left_img, True, False)
    arrow_right_rect = pygame.Rect(WIDTH // 1.12, HEIGHT // 2.3, arrow_w, arrow_h)
    screen.blit(arrow_right_img, arrow_right_rect)
    arrow_positions = [arrow_left_rect, arrow_right_rect]
    pygame.display.flip()
    return button_positions, arrow_positions, input_box, skin_choice


def draw_question(question: Question, chosen_answer: str, next_coordinate: tuple[int, int], question_type: str, game: Game):

    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    question_width = WIDTH // 1.2
    question_height = HEIGHT // 1.4
    question_rect = pygame.Rect(0, 0, question_width, question_height)
    question_rect.center = (WIDTH // 2, HEIGHT // 2)

    if chosen_answer == '':
        pygame.draw.rect(surface, LIGHTGRAY, question_rect, 0, 20)
        answered = False
    else:
        if chosen_answer == question.answer.lower()[0]:
            pygame.draw.rect(surface, GREEN, question_rect, 0, 20)
            answered = 'right'
            audio.correct.play(loops=1)
        else:
            pygame.draw.rect(surface, DARKRED, question_rect, 0, 20)
            answered = 'wrong'
            audio.wrong.play()
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

    if len(question.question) < 30:
        title = subfont.render(question.question, True, WHITE)
        title_rect = title.get_rect()
        title_rect.top = HEIGHT//4
        title_rect.centerx = WIDTH//2
        surface.blit(title, title_rect)
    else:
        count = 0
        for i in range(len(question.question), 0, -1):
            if question.question[i-1] == " ":
                count += 1
            if count == 3:
                part1 = question.question[0:i]
                part2 = question.question[i:len(question.question)]
                break

        draw_title(part1, subfont, WHITE, surface, question=1)
        draw_title(part2, subfont, WHITE, surface, question=2)

    button_text = [question.a, question.b, question.c, question.d]
    answer_buttons:list[pygame.Rect] = []
    buttonx = [WIDTH // 7, WIDTH // 1.9]
    buttony = [HEIGHT // 2.4, HEIGHT // 1.6]
    button_height = HEIGHT // 8
    textfont = pygame.font.Font(None, WIDTH // 30)

    for i in range(4):
        text_surface = textfont.render(button_text[i], True, button_textcolor)
        if i == 0:
            text_rect = text_surface.get_rect(center=(buttonx[i] + (button_width / 2), buttony[i] + (button_height / 2)))
            rect = pygame.draw.rect(surface, button_backgroundcolor, (buttonx[i], buttony[i], button_width, button_height))
        elif i == 1:
            text_rect = text_surface.get_rect(center=(buttonx[i] + (button_width / 2), buttony[0] + (button_height / 2)))
            rect = pygame.draw.rect(surface, button_backgroundcolor, (buttonx[i], buttony[0], button_width, button_height))
        elif i == 2:
            text_rect = text_surface.get_rect(center=(buttonx[0] + (button_width / 2), buttony[1] + (button_height / 2)))
            rect = pygame.draw.rect(surface, button_backgroundcolor, (buttonx[0], buttony[1], button_width, button_height))
        else:
            text_rect = text_surface.get_rect(center=(buttonx[1] + (button_width / 2), buttony[1] + (button_height / 2)))
            rect = pygame.draw.rect(surface, button_backgroundcolor, (buttonx[1], buttony[1], button_width, button_height))
        surface.blit(text_surface, text_rect)
        answer_buttons.append(rect)

    screen.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()

    return answer_buttons, answered
