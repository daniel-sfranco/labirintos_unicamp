import pygame
from constants import *
from pygame.font import Font
from save import return_saves
from student import get_history
import audio
from player import Player
from game_generator import Game
from manage import Manager


def draw_init() -> list[pygame.Rect]:
    """
    Initializes the game screen by filling it with a background color, drawing the game title,
    creating menu buttons, and updating the display. Returns the positions of the buttons as a list of pygame.Rect objects.
    """
    screen.fill(BACKGROUND)
    draw_title('LABIRINTOS DA UNICAMP', titlefont, WHITE)

    button_text = ['Novo Jogo', 'Carregar Jogo', 'Exibir Histórico', 'Informações', 'Sair']
    button_positions: list[pygame.Rect] = draw_menu(button_text, 3)

    pygame.display.flip()

    return button_positions


def draw_menu(button_text: list[str], div: float, surface: pygame.Surface = SCREEN) -> list[pygame.Rect]:
    """
    Create and display a series of buttons on a Pygame surface.

    Args:
        button_text (list[str]): A list of strings representing the text on each button.
        div (float): A value used to calculate the vertical position of the buttons.
        surface (pygame.Surface, optional): Pygame surface where buttons will be drawn. Defaults to SCREEN.

    Returns:
        list[pygame.Rect]: A list of pygame.Rect objects representing button positions.
    """
    num_buttons = len(button_text)
    button_x = (WIDTH - button_width) / 2
    button_y = [round(HEIGHT / div) + i * button_distance for i in range(num_buttons)]
    button_positions: list[pygame.Rect] = []

    for i, text in enumerate(button_text):
        text_surface = textfont.render(text, True, button_textcolor)
        text_rect = text_surface.get_rect(center=(button_x + (button_width / 2), button_y[i] + (button_height / 2)))

        pygame.draw.rect(surface, button_backgroundcolor, (button_x, button_y[i], button_width, button_height))
        surface.blit(text_surface, text_rect)

        button_positions.append(pygame.Rect(button_x, button_y[i], button_width, button_height))

    return button_positions


def draw_title_button(title_text: str) -> pygame.Rect:
    # Create a transparent surface
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Draw a black rectangle covering the entire surface
    pygame.draw.rect(surface, BLACK, [0, 0, WIDTH, HEIGHT])

    # Render the title text using a specific font and draw it on the surface
    font = pygame.font.Font('./fonts/PixelTimes.ttf', 24)
    text_surface = font.render(title_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    surface.blit(text_surface, text_rect)

    # Define the button's dimensions and position
    button_w = WIDTH // 3
    button_h = HEIGHT // 1.5
    button_x = WIDTH // 12
    button_y = HEIGHT // 1.15

    # Render the button text and draw the button rectangle
    button_text = 'Voltar'
    button_text_surface = font.render(button_text, True, button_textcolor)
    button_text_rect = button_text_surface.get_rect(center=(button_x + button_w // 2, button_y + button_h // 2))
    pygame.draw.rect(surface, button_backgroundcolor, (button_x, button_y, button_w, button_h))
    surface.blit(button_text_surface, button_text_rect)

    # Blit the entire surface onto the main screen
    screen.blit(surface, (0, 0))

    # Return the button's rectangle
    return pygame.Rect(button_x, button_y, button_w, button_h)


def draw_title(text: str, font: Font, color, surface: pygame.Surface = SCREEN, back=BLACK, question=0) -> None:
    """
    Render a title text on a Pygame surface with optional background color and positioning based on the context.

    Args:
        text (str): The title text to be displayed.
        font (Font): The Pygame font object used to render the text.
        color: The color of the text.
        surface (pygame.Surface, optional): The Pygame surface where the text will be drawn. Defaults to SCREEN.
        back: The background color for the text rectangle. Defaults to BLACK.
        question (int, optional): An integer to adjust the vertical position of the text. Defaults to 0.
    """
    title = font.render(text, True, color)
    title_rect = title.get_rect(center=(WIDTH // 2, {0: HEIGHT // 10, 1: HEIGHT // 5, 2: round(HEIGHT / 3.5)}.get(question)))
    pygame.draw.rect(surface, back, title_rect.inflate(60, 40), border_radius=20)
    surface.blit(title, title_rect)


def draw_select_save(type: str = 'load', player: Player = Player(''), game: Game = Game(1), manager = Manager()) -> list[pygame.Rect]:
    """
    Create a graphical interface for selecting a saved game to load or delete.

    Args:
        type (str): Type of action ('load' or 'delete').
        player (Player): Current player instance.
        game (Game): Current game state instance.
        manager (Manager): Game state manager instance.

    Returns:
        list[pygame.Rect]: List of pygame.Rect objects representing menu button positions.
    """
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])

    if type == 'load':
        pygame.draw.rect(surface, BLACK, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo salvo', subfont, WHITE, surface)
    elif type == 'delete':
        draw_maze(player, game, manager)
        pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo para sobreescrever', subfont, WHITE, surface)
        pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)

    games = return_saves()
    button_text = [f'{save[2].name}: nível {save[1].level}, {save[2].lives} vidas' for save in games]
    button_text.extend(['Limpar jogos salvos', 'Voltar'])

    menu: list[pygame.Rect] = draw_menu(button_text, 3.5, surface)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    return menu


def draw_pause_button() -> pygame.Rect:
    """
    Create and display a pause button on the game screen.

    Returns:
    pygame.Rect: Rectangle representing the position and size of the pause button.
    """
    button_size = FIRST_UNIT // 4
    pause_img = pygame.transform.scale(pygame.image.load('img/arrowRight.png').convert(), (button_size, button_size))
    pause_rect = pause_img.get_rect(topleft=(WIDTH - 2 * button_size, button_size))
    screen.blit(pause_img, pause_rect)
    return pause_rect


def draw_maze(player: Player, game: Game, manager: Manager) -> None:
    """
    Render the maze, player, and game elements on the screen.

    Args:
        player (Player): An instance of the Player class representing the player.
        game (Game): An instance of the Game class representing the current game state.
        manager (Manager): An instance of the Manager class managing game states and assets.

    Returns:
        None
    """
    screen.fill(BACKGROUND)
    maze = game.maze
    maze_size = len(maze)
    maze_surface = pygame.Surface((game.unit_size * maze_size, game.unit_size * len(maze[0])))
    maze_surface.fill(TILE_COLOR)

    player.img = pygame.transform.scale(player.img, (game.unit_size, game.unit_size))
    player_y = player.coordinate[0] * game.unit_size
    player_y, game.player_dif = adjust_player_position(player_y, game.unit_size, maze_size)

    wall = pygame.transform.scale(WALL, (game.unit_size, game.unit_size))
    floor = pygame.transform.scale(FLOOR, (game.unit_size, game.unit_size))
    ghost = pygame.transform.scale(GHOST, (game.unit_size, game.unit_size))
    teacher = pygame.transform.scale(PROF, (game.unit_size, game.unit_size))
    bomb = pygame.transform.scale(manager.bomb_sprite.image, (game.unit_size, game.unit_size))
    point = pygame.transform.scale(POINT, (game.unit_size // 2, game.unit_size // 2))
    life = pygame.transform.scale(HEART, (game.unit_size, game.unit_size))
    clock = pygame.transform.scale(CLOCK_ICON, (game.unit_size, game.unit_size))

    for y in range(0, len(maze) * game.unit_size, game.unit_size):
        for x in range(0, len(maze[0]) * game.unit_size, game.unit_size):
            maze_y, maze_x = y // game.unit_size, x // game.unit_size
            maze_surface.blit(floor, (x, y - game.player_dif))
            if maze[maze_y][maze_x] == 1:
                maze_surface.blit(wall, (x, y - game.player_dif))
            else:
                draw_game_elements(maze, maze_y, maze_x, x, y, game, manager, maze_surface, ghost, teacher, bomb, point, life, clock, game.unit_size, game.player_dif, player.img)
    screen.blit(maze_surface, (0, 0))


def adjust_player_position(player_y: int, unit_size: int, maze_size: int) -> tuple[int, int]:
    """
    Adjusts the vertical position of the player within the maze to keep the player centered on the screen.

    Args:
        player_y (int): The current vertical position of the player in pixels.
        unit_size (int): The size of one unit (tile) in the maze in pixels.
        maze_size (int): The total number of units (tiles) in the maze vertically.

    Returns:
        Tuple[int, int]: The adjusted vertical position of the player and the total adjustment made.
    """
    dif = 0
    max_height = maze_size * unit_size
    while player_y > HEIGHT // 2 and max_height > HEIGHT:
        dif += unit_size
        player_y -= unit_size
        max_height -= unit_size
    return player_y, dif


def draw_game_elements(maze: list, maze_y: int, maze_x: int, x: int, y: int, game, manager, maze_surface: pygame.Surface, ghost: pygame.Surface, teacher: pygame.Surface, bomb: pygame.Surface, point: pygame.Surface, life: pygame.Surface, clock: pygame.Surface, unit_size: int, player_dif: int, img: pygame.Surface) -> None:
    """
    Renders various game elements on the maze surface based on the maze's tile type at specific coordinates.

    Args:
    maze (list): The maze structure containing different tile types.
    maze_y (int): The y-coordinate in the maze.
    maze_x (int): The x-coordinate in the maze.
    x (int): The x-coordinate on the surface.
    y (int): The y-coordinate on the surface.
    game (Any): The game instance containing game-related data.
    manager (Any): The manager instance handling game states and assets.
    maze_surface (pygame.Surface): The surface where the maze is drawn.
    ghost (pygame.Surface): Image for ghost.
    teacher (pygame.Surface): Image for teacher.
    bomb (pygame.Surface): Image for bomb.
    point (pygame.Surface): Image for point.
    life (pygame.Surface): Image for life.
    clock (pygame.Surface): Image for clock.
    unit_size (int): Size of the game elements.
    player_dif (int): Player difference.
    img (pygame.Surface): General image for other elements.
    """
    tile_type: dict[str, pygame.Surface] = {'s': ghost, 't': teacher, 'n': point, 'l': life, 'c': clock, 'p': img}

    if isinstance(maze[maze_y][maze_x], str):
        for i in maze[maze_y][maze_x]:
            if i == 'n':
                maze_surface.blit(tile_type[i], (x + (unit_size // 4), y - player_dif + (unit_size // 4)))
            elif i == 'a':
                continue
            elif i == 'b':
                maze_surface.blit(bomb, (x, y - player_dif))
                manager.bomb_sprite.update()
            else:
                maze_surface.blit(tile_type[i], (x, y - player_dif))


def draw_HUD(player: Player, game: Game) -> None:
    hud = pygame.Surface((SIZE), pygame.SRCALPHA)
    hud_height = HEIGHT // 1.3
    hud_y = ((HEIGHT * 1.05) - hud_height) / 2
    hud_width = WIDTH // 4.5
    hud_x = (WIDTH - hud_width) / 1.02
    pygame.draw.rect(hud, DARKGRAY, [hud_x, hud_y, hud_width, hud_height])
    text = [f"Labirinto: {game.level}", f"Pontos: {game.points}", f"Total: {player.points}", f"Tempo: {game.time}", f"S2: {player.lives}", f"Bombas: {player.bombs}"]
    font = Font('./fonts/dogicapixel.ttf', WIDTH // 60)
    mini_size = FIRST_UNIT * 0.35
    size = (mini_size, mini_size)
    for i in range(len(text)):
        if i == 4:
            icon = pygame.transform.scale(HEART, size)
            for j in range(player.lives):
                heart_rect = pygame.Rect(hud_x + (hud_width / (i + 1.8)) + j * mini_size, hud_y + (hud_height / height_div), mini_size, mini_size)
                hud.blit(icon, heart_rect)
        elif i == 5:
            icon = pygame.transform.scale(BOMB, size)
            for j in range(player.bombs):
                bomb_rect = pygame.Rect(hud_x + (hud_width / (i + 0.8)) + j * mini_size, hud_y + (hud_height / (height_div / 1.2)), mini_size, mini_size)
                hud.blit(icon, bomb_rect)
        else:
            height_div = (6 / (i + 1))
            text_surface = font.render(text[i], True, WHITE)
            text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 2.2), hud_y + (hud_height / (height_div + 0.3))))
            hud.blit(text_surface, text_rect)
    screen.blit(hud, (0, 0))


def draw_pause_menu(player: Player, game: Game, manager: Manager) -> list[pygame.Rect]:
    draw_maze(player, game, manager)
    draw_HUD(player, game)
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, GRAY, [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y, menu_width, menu_height], 0, 20)
    button_text = ['Voltar', 'Reiniciar labirinto atual', 'Salvar', 'Novo jogo', 'Sair']
    draw_title('Pausado', subfont, WHITE, surface=surface)
    menu = draw_menu(button_text, 3.5, surface)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))
    return menu


def draw_game_over(game: Game, player: Player, manager: Manager) -> list[pygame.Rect]:
    draw_maze(player, game, manager)
    draw_HUD(player, game)
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, RED, [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BLACK, [menu_x, menu_y * 1.3, menu_width, menu_height * 0.7], 0, 20)
    button_text = ['Novo jogo', 'Exibir ganhadores', 'Sair']
    draw_title('FIM DE JOGO', titlefont, WHITE, surface, BLACK)
    menu = draw_menu(button_text, 2.65, surface)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))
    return menu


def draw_character_sel(manager: Manager) -> tuple[list[pygame.Rect], list[pygame.Rect], pygame.Rect, str]:
    char_button_w = button_width * 0.3
    char_button_h = button_height * 0.6
    screen.fill(BACKGROUND)
    draw_title('SELECIONE SEU PERSONAGEM', titlefont, WHITE)
    button_x = [WIDTH // 8, WIDTH // 1.3]
    button_y = HEIGHT // 1.2

    font = Font('./fonts/PixelTimes.ttf', 24)
    input_box = pygame.Rect(WIDTH / 3, button_y, WIDTH // 3, button_height * 0.6)
    background_inactive = pygame.Color(BACKGROUND)
    background_active = pygame.Color(WHITE)
    color_active = background_inactive
    color_inactive = background_active
    if manager.input_active:
        color = color_active
        background = background_active
    else:
        color = color_inactive
        background = background_inactive
    if manager.input_active is False and manager.user_input == "":
        input_text = font.render("Escolha o nome do seu personagem", True, color)
    else:
        input_text = font.render(manager.user_input, True, color)
    input_rect = input_text.get_rect(center=(input_box.centerx, input_box.centery))
    pygame.draw.rect(screen, background, input_box)
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
        slide_x = (WIDTH // 2.5 - (character_distance * manager.skin_sel)) + i * character_distance
        if i == manager.skin_sel:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + CHARACTERS[i] + '.gif'), (11, 11))
        else:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + CHARACTERS[i] + '.gif').convert_alpha(), (8, 8))
            darken_surface = pygame.Surface(character_img.get_size()).convert_alpha()
            darken_surface.fill((255, 255, 255, 150))
            character_img.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        character_rect = pygame.Rect(slide_x, slide_y, character_w, character_h)
        screen.blit(character_img, character_rect)

    skin_choice: str = CHARACTERS[manager.skin_sel]

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


def draw_question(manager: Manager, game: Game):
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    question_rect = pygame.Rect(0, 0, WIDTH // 1.2, HEIGHT // 1.4)
    question_rect.center = (WIDTH // 2, HEIGHT // 2)
    if manager.chosen_answer == '':
        color = LIGHTGRAY
        answered = False
    else:
        if manager.chosen_answer == manager.question.answer.lower()[0]:
            color = GREEN
            answered = 'right'
            audio.correct.play(loops=1)
        else:
            color = DARKRED
            answered = 'wrong'
            audio.wrong.play()
    pygame.draw.rect(surface, color, question_rect, 0, 20)
    screen.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

    subfont = pygame.font.Font('./fonts/dogicapixelbold.ttf', WIDTH // 45)
    pos = []
    for i in range(len(manager.question.question), 0, -1):
        if manager.question.question[i - 1] == " ":
            pos.append(i)
    if len(pos) < 7:
        title = subfont.render(manager.question.question, True, WHITE)
        title_rect = title.get_rect()
        title_rect.top, title_rect.centerx = (HEIGHT // 4, WIDTH // 2)
        surface.blit(title, title_rect)
    else:
        part1 = manager.question.question[0:pos[len(pos) // 2]]
        part2 = manager.question.question[pos[len(pos) // 2]:len(manager.question.question)]
        draw_title(part1, subfont, WHITE, surface, question=1, back=color)
        draw_title(part2, subfont, WHITE, surface, question=2, back=color)
    button_text = [manager.question.a, manager.question.b, manager.question.c, manager.question.d]
    answer_buttons: list[pygame.Rect] = []
    buttonx = [WIDTH // 7, WIDTH // 1.9]
    buttony = [HEIGHT // 2.4, HEIGHT // 1.6]
    button_height = HEIGHT // 8

    for i in range(4):
        text_surface = textfont.render(button_text[i], True, button_textcolor)
        text_rect = text_surface.get_rect(center=(buttonx[i % 2] + (button_width / 2), buttony[i // 2] + (button_height / 2)))
        rect = pygame.draw.rect(surface, button_backgroundcolor, (buttonx[i % 2], buttony[i // 2], button_width, button_height))
        surface.blit(text_surface, text_rect)
        answer_buttons.append(rect)
    screen.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()
    return answer_buttons, answered


def draw_winners(game) -> pygame.Rect:
    back_button = draw_title_button('Histórico')
    studentes_ordered = get_history()
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)

    players = len(studentes_ordered)
    if players > 5:
        players = 5

    card_width = menu_width
    card_height = menu_height * 0.2
    card_x = (WIDTH - card_width) / 2
    card_y = HEIGHT - card_width

    for i in range(players):
        pygame.draw.rect(surface, WHITE, [menu_x, ((menu_y * 0.8) + (i * 150)), card_width, card_height], 2)

        text_position = textfont.render(f'{(i + 1)}. {studentes_ordered[i].name[:-1]}', True, WHITE)
        text_rect = text_position.get_rect(topleft=(WIDTH / 3.25, (card_y*0.7)+(i*150)))
        surface.blit(text_position, text_rect)

        text_points = textfont.render(f'Pontuação: {studentes_ordered[i].points}', True, WHITE)
        text_rect = text_position.get_rect(bottomleft=(WIDTH / 3.25, (card_y)+(i*150)))
        surface.blit(text_points, text_rect)

        text_level = textfont.render(f'Último labirinto: {studentes_ordered[i].level}', True, WHITE)
        text_rect = text_position.get_rect(bottomleft=(WIDTH / 2, (card_y)+(i*150)))
        surface.blit(text_level, text_rect)

    screen.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()

    return back_button


def draw_info() -> pygame.Rect:
    back_button = draw_title_button('Informações')

    pygame.display.flip()
    return back_button