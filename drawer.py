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
    Initializes the game SCREEN by filling it with a background color, drawing the game title,
    creating menu buttons, and updating the display. Returns the positions of the buttons as a list of pygame.Rect objects.
    """
    SCREEN.fill(BACKGROUND)
    draw_title('LABIRINTOS DA UNICAMP', TITLEFONT, TITLE_COLOR)

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
    button_x = (WIDTH - BUTTON_WIDTH) / 2
    button_y = [round(HEIGHT / div) + i * BUTTON_DISTANCE for i in range(num_buttons)]
    button_positions: list[pygame.Rect] = []

    for i, text in enumerate(button_text):
        text_surface = TEXTFONT.render(text, True, BUTTON_TEXTCOLOR)
        text_rect = text_surface.get_rect(center=(button_x + (BUTTON_WIDTH / 2), button_y[i] + (BUTTON_HEIGHT / 2)))

        pygame.draw.rect(surface, BUTTON_BACKGROUNDCOLOR, (button_x, button_y[i], BUTTON_WIDTH, BUTTON_HEIGHT))
        surface.blit(text_surface, text_rect)

        button_positions.append(pygame.Rect(button_x, button_y[i], BUTTON_WIDTH, BUTTON_HEIGHT))

    return button_positions


def draw_back_button(title_text: str) -> pygame.Rect:
    """
    Create a back button on a Pygame surface with a title and return the button's rectangle.

    Args:
        title_text (str): The title text to be displayed at the top of the SCREEN.

    Returns:
        pygame.Rect: A rectangle representing the back button's position and size.
    """
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, BACKGROUND, [0, 0, WIDTH, HEIGHT])

    draw_title(title_text, TEXTFONT, TITLE_COLOR, surface, BACKGROUND, 0, 10)

    button_w, button_h = WIDTH // 6, HEIGHT // 12
    button_x, button_y = WIDTH // 12, HEIGHT // 1.15

    button_text = 'Voltar'
    button_text_surface = TEXTFONT.render(button_text, True, BUTTON_TEXTCOLOR)
    button_text_rect = button_text_surface.get_rect(center=(button_x + button_w // 2, button_y + button_h // 2))
    pygame.draw.rect(surface, BUTTON_BACKGROUNDCOLOR, (button_x, button_y, button_w, button_h))
    surface.blit(button_text_surface, button_text_rect)

    SCREEN.blit(surface, (0, 0))

    return pygame.Rect(button_x, button_y, button_w, button_h)


def draw_title(text: str, font: Font, color, surface: pygame.Surface = SCREEN, back=BACKGROUND, question=0, div=10) -> None:
    """
    Render a title text on a Pygame surface with optional background color and positioning based on the context.

    Args:
        text (str): The title text to be displayed.
        font (Font): The Pygame font object used to render the text.
        color: The color of the text.
        surface (pygame.Surface, optional): The Pygame surface where the text will be drawn. Defaults to SCREEN.
        back: The background color for the text rectangle. Defaults to BACKGROUND.
        question (int, optional): An integer to adjust the vertical position of the text. Defaults to 0.
    """
    title = font.render(text, True, color)
    dif = 220 if question > 0 else 0
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // div - 60 * question + dif))
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

    if type == 'load':
        pygame.draw.rect(surface, BACKGROUND, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo salvo', TITLEFONT, TITLE_COLOR, surface)
    elif type == 'delete':
        draw_maze(player, game, manager)
        pygame.draw.rect(surface, FADED_COLOR, [0, 0, WIDTH, HEIGHT])
        draw_title('Escolha um jogo para sobreescrever', SUBFONT, TITLE_COLOR, surface)
        pygame.draw.rect(surface, BACKGROUND, [MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT], 0, 20)

    games = return_saves()
    button_text = [f'{save[2].name}: nível {save[1].level}, {save[2].lives} vidas' for save in games]
    button_text.extend(['Limpar jogos salvos', 'Voltar'])

    menu: list[pygame.Rect] = draw_menu(button_text, 3.5, surface)
    SCREEN.blit(surface, (0, 0))
    pygame.display.flip()

    return menu


def draw_pause_button() -> pygame.Rect:
    """
    Create and display a pause button on the game SCREEN.

    Returns:
    pygame.Rect: Rectangle representing the position and size of the pause button.
    """
    button_size = FIRST_UNIT // 4
    pause_img = pygame.transform.scale(pygame.image.load('img/arrowRight.png').convert(), (button_size, button_size))
    pause_rect = pause_img.get_rect(topleft=(WIDTH - 2 * button_size, button_size))
    SCREEN.blit(pause_img, pause_rect)
    return pause_rect


def draw_maze(player: Player, game: Game, manager: Manager) -> None:
    """
    Renders the maze and its elements on the SCREEN.

    Args:
        player (Player): An instance of the Player class representing the player.
        game (Game): An instance of the Game class containing the maze and game-related data.
        manager (Manager): An instance of the Manager class handling game states and assets.

    Returns:
        None
    """
    SCREEN.fill(BACKGROUND)
    maze = game.maze
    maze_size = len(maze)
    maze_surface = pygame.Surface((game.unit_size * maze_size, game.unit_size * len(maze[0])))

    player_y = player.coordinate[0] * game.unit_size
    player_y, game.player_dif = adjust_player_position(player_y, game.unit_size, maze_size)
    sprites = {
        'player_img': pygame.transform.scale(player.img, (game.unit_size, game.unit_size)),
        'wall': pygame.transform.scale(WALL, (game.unit_size, game.unit_size)),
        'floor': pygame.transform.scale(FLOOR, (game.unit_size, game.unit_size)),
        'ghost': pygame.transform.scale(GHOST, (game.unit_size, game.unit_size)),
        'teacher': pygame.transform.scale(PROF, (game.unit_size, game.unit_size)),
        'act_bomb': pygame.transform.scale(manager.bomb_sprite.image, (game.unit_size, game.unit_size)),
        'point': pygame.transform.scale(POINT, (game.unit_size // 2, game.unit_size // 2)),
        'life': pygame.transform.scale(HEART, (game.unit_size, game.unit_size)),
        'clock': pygame.transform.scale(CLOCK_ICON, (game.unit_size, game.unit_size)),
        'door': pygame.transform.scale(DOOR, (game.unit_size, game.unit_size)),
        'bomb': pygame.transform.scale(BOMB, (game.unit_size, game.unit_size))
    }

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            maze_y, maze_x = y * game.unit_size, x * game.unit_size
            if cell == 1:
                maze_surface.blit(sprites['wall'], (maze_x, maze_y - game.player_dif))
            else:
                maze_surface.blit(sprites['floor'], (maze_x, maze_y - game.player_dif))
                if y == maze_size - 1 and x == len(row) - 1:
                    maze_surface.blit(sprites['door'], (maze_x, maze_y - game.player_dif))
                draw_game_elements(game, x, y, manager, maze_surface, sprites)
    SCREEN.blit(maze_surface, (0, 0))


def adjust_player_position(player_y: int, unit_size: int, maze_size: int) -> tuple[int, int]:
    """
    Adjusts the vertical position of the player within the maze to keep the player centered on the SCREEN.

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


def draw_game_elements(game: Game, x: int, y: int, manager, maze_surface: pygame.Surface, sprites: dict[str, pygame.Surface]) -> None:
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
    tile_type: dict[str, pygame.Surface] = {'s': sprites['ghost'], 'b': sprites['bomb'], 't': sprites['teacher'], 'n': sprites['point'], 'l': sprites['life'], 'c': sprites['clock'], 'p': sprites['player_img']}
    tile_type: dict[str, pygame.Surface] = {'s': sprites['ghost'], 't': sprites['teacher'], 'n': sprites['point'], 'l': sprites['life'], 'c': sprites['clock'], 'p': sprites['player_img'], 'b': sprites['bomb']}
    maze_y, maze_x = y * game.unit_size, x * game.unit_size
    if isinstance(game.maze[y][x], str):
        for i in game.maze[y][x]:
            if i == 'n':
                maze_surface.blit(tile_type[i], (maze_x + (game.unit_size // 4), maze_y - game.player_dif + (game.unit_size // 4)))
            elif i == 'x':
                maze_surface.blit(sprites['act_bomb'], (maze_x, maze_y - game.player_dif))
                manager.bomb_sprite.update(game)
            else:
                maze_surface.blit(tile_type[i], (maze_x, maze_y - game.player_dif))


def draw_HUD(player: Player, game: Game) -> None:
    """
    Renders the Heads-Up Display (HUD) for the game.

    Args:
        player (Player): An instance of the Player class.
        game (Game): An instance of the Game class.

    Returns:
        None
    """
    hud = pygame.Surface((SIZE), pygame.SRCALPHA)
    hud_height = HEIGHT // 1.3
    hud_y = ((HEIGHT * 1.05) - hud_height) / 2
    hud_width = WIDTH // 4.5
    hud_x = (WIDTH - hud_width) / 1.02
    pygame.draw.rect(hud, HUD_COLOR, [hud_x, hud_y, hud_width, hud_height], 0, 10)

    text = [f"Labirinto: {game.level}", f"Pontos: {game.points}", f"Total: {player.points}",
            f"Tempo: {game.time}", f"S2: {player.lives}", f"Bombas: {player.bombs}"]

    font = Font('./fonts/dogicapixel.ttf', WIDTH // 60)
    mini_size = FIRST_UNIT * 0.35
    size = (mini_size, mini_size)

    for i, item in enumerate(text):
        if i == 4:
            icon = pygame.transform.scale(HEART, size)
            if player.lives <= 3:
                for j in range(player.lives):
                    heart_rect = pygame.Rect(hud_x + (hud_width / (i + 3)) + j * mini_size,
                                        hud_y + (hud_height / (6 / (i))), mini_size, mini_size)
                    hud.blit(icon, heart_rect)
            else:
                for j in range(3):
                    heart_rect = pygame.Rect(hud_x + (hud_width / (i + 1.8)) + j * mini_size, hud_y + (hud_height / height_div), mini_size, mini_size)
                    hud.blit(icon, heart_rect)
                text_surface = font.render(f'+ {player.lives-3}', True, TITLE_COLOR)
                text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 1.3), hud_y + (hud_height / 1.42)))
                hud.blit(text_surface, text_rect)
        elif i == 5:
            icon = pygame.transform.scale(BOMB, size)
            if player.bombs <= 3:
                for j in range(player.bombs):
                    bomb_rect = pygame.Rect(hud_x + (hud_width / (i + 2)) + j * mini_size,
                                        hud_y + (hud_height / (6 / (i - 0.1))), mini_size, mini_size)
                    hud.blit(icon, bomb_rect)
            else:
                for j in range(3):
                    bomb_rect = pygame.Rect(hud_x + (hud_width / (i + 0.8)) + j * mini_size, hud_y + (hud_height / (height_div / 1.2)), mini_size, mini_size)
                    hud.blit(icon, bomb_rect)
                text_surface = font.render(f'+ {player.bombs-3}', True, TITLE_COLOR)
                text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 1.3), hud_y + (hud_height / 1.17)))
                hud.blit(text_surface, text_rect)
        else:
            height_div = (6 / (i + 1))
            text_surface = font.render(item, True, TITLE_COLOR)
            text_rect = text_surface.get_rect(center=(hud_x + (hud_width / 2.2), hud_y + (hud_height / (height_div + 0.3))))
            hud.blit(text_surface, text_rect)

    SCREEN.blit(hud, (0, 0))


def draw_pause_menu(player: Player, game: Game, manager: Manager) -> list[pygame.Rect]:
    """
    Renders the pause menu overlay on the game SCREEN.

    Args:
        player (Player): An instance of the Player class representing the player.
        game (Game): An instance of the Game class containing the maze and game-related data.
        manager (Manager): An instance of the Manager class handling game states and assets.

    Returns:
        list[pygame.Rect]: A list of pygame.Rect objects representing the positions of the menu buttons.
    """
    draw_maze(player, game, manager)
    draw_HUD(player, game)

    # Create a semi-transparent overlay
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, FADED_COLOR, surface.get_rect())

    # Draw menu background
    pygame.draw.rect(surface, BACKGROUND, (MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT), 0, 20)

    # Display menu options
    button_text = ['Voltar', 'Reiniciar labirinto atual', 'Salvar', 'Novo jogo', 'Sair']
    draw_title('Pausado', SUBFONT, TITLE_COLOR, surface=surface)
    menu = draw_menu(button_text, 3.5, surface)

    # Blit overlay onto the main SCREEN
    SCREEN.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

    return menu


def draw_game_over(game: Game, player: Player, manager: Manager) -> list[pygame.Rect]:
    """
    Renders the game over SCREEN with maze, HUD, and menu options.

    Args:
        game (Game): An instance of the Game class containing the current game state.
        player (Player): An instance of the Player class representing the player.
        manager (Manager): An instance of the Manager class handling game states and assets.

    Returns:
        list[pygame.Rect]: A list of pygame.Rect objects representing the positions of the menu buttons.
    """
    draw_maze(player, game, manager)
    draw_HUD(player, game)

    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surface, COLORS['RED'], [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, BACKGROUND, [MENU_X, MENU_Y * 1.3, MENU_WIDTH, MENU_HEIGHT * 0.7], 0, 20)

    button_text = ['Novo jogo', 'Exibir histórico', 'Sair']
    draw_title('FIM DE JOGO', TITLEFONT, TITLE_COLOR, surface)
    menu = draw_menu(button_text, 2.65, surface)

    SCREEN.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))
    return menu


def draw_character_sel(manager: Manager) -> tuple[list[pygame.Rect], list[pygame.Rect], pygame.Rect, str]:
    """
    Renders a character selection SCREEN in a Pygame application.

    Displays a title, input box for character name, navigation buttons, and character images.
    Handles the visual feedback for the selected character and navigation arrows.

    Args:
        manager (Manager): An instance of the Manager class containing the state of the game and user inputs.

    Returns:
        tuple: A tuple containing button positions, arrow positions, input box position, and the selected character.
    """
    SCREEN.fill(BACKGROUND)
    draw_title('SELECIONE SEU PERSONAGEM', TITLEFONT, TITLE_COLOR)

    char_button_w = BUTTON_WIDTH * 0.3
    char_button_h = BUTTON_HEIGHT * 0.6
    button_x = [WIDTH // 8, WIDTH // 1.3]
    button_y = HEIGHT // 1.2
    button_text = ['Voltar', 'Concluir']
    button_positions: list[pygame.Rect] = []

    font = Font('./fonts/PixelTimes.ttf', 24)
    background_inactive = pygame.Color(BACKGROUND)
    background_active = pygame.Color(TITLE_COLOR)
    color_active = background_inactive
    color_inactive = background_active
    color = color_active if manager.input_active else color_inactive

    input_box = pygame.Rect(WIDTH / 3, button_y, WIDTH // 3, BUTTON_HEIGHT * 0.6)
    input_text = font.render("Escolha o nome do seu personagem" if not manager.input_active and not manager.user_input else manager.user_input, True, color)
    input_rect = input_text.get_rect(center=(input_box.centerx, input_box.centery))
    pygame.draw.rect(SCREEN, background_active if manager.input_active else background_inactive, input_box)
    SCREEN.blit(input_text, input_rect)

    for i, text in enumerate(button_text):
        text_surface = font.render(text, True, BUTTON_TEXTCOLOR)
        text_rect = text_surface.get_rect(center=(button_x[i] + (char_button_w / 2), button_y + (char_button_h / 2)))
        pygame.draw.rect(SCREEN, BUTTON_BACKGROUNDCOLOR, (button_x[i], button_y, char_button_w, char_button_h))
        SCREEN.blit(text_surface, text_rect)
        button_positions.append(pygame.Rect(button_x[i], button_y, char_button_w, char_button_h))

    slide_y = HEIGHT // 4
    character_w = FIRST_UNIT // 0.5
    character_h = FIRST_UNIT // 0.4
    character_distance = 600
    for i, character in enumerate(CHARACTERS):
        slide_x = (WIDTH // 2.5 - (character_distance * manager.skin_sel)) + i * character_distance
        if i == manager.skin_sel:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + character + '.gif'), (11, 11))
        else:
            character_img = pygame.transform.scale_by(pygame.image.load('img/player/' + character + '.gif').convert_alpha(), (8, 8))
            darken_surface = pygame.Surface(character_img.get_size()).convert_alpha()
            darken_surface.fill((255, 255, 255, 150))
            character_img.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        character_rect = pygame.Rect(slide_x, slide_y, character_w, character_h)
        SCREEN.blit(character_img, character_rect)

    skin_choice: str = CHARACTERS[manager.skin_sel]

    arrow_w = FIRST_UNIT // 4
    arrow_h = FIRST_UNIT // 2
    arrow_left_img = pygame.transform.scale(pygame.image.load('img/arrowLeft.png'), (arrow_w, arrow_h))
    arrow_left_rect = pygame.Rect(WIDTH // 12, HEIGHT // 2.3, arrow_w, arrow_h)
    arrow_right_img = pygame.transform.flip(arrow_left_img, True, False)
    arrow_right_rect = pygame.Rect(WIDTH // 1.12, HEIGHT // 2.3, arrow_w, arrow_h)
    arrow_positions = [arrow_left_rect, arrow_right_rect]

    SCREEN.blit(arrow_left_img, arrow_left_rect)
    SCREEN.blit(arrow_right_img, arrow_right_rect)
    pygame.display.flip()

    return button_positions, arrow_positions, input_box, skin_choice


def draw_question(manager: Manager, game: Game):
    """
    Renders a question interface on the SCREEN, displaying the question text and answer buttons.
    Handles visual feedback for correct or incorrect answers by changing the background color and playing audio effects.

    Args:
        manager (Manager): An instance of the Manager class containing game state and question details.
        game (Game): An instance of the Game class representing the current game state.

    Returns:
        tuple: A tuple containing a list of pygame.Rect objects representing the answer buttons and a boolean or string
        indicating whether the question was answered correctly, incorrectly, or not at all.
    """
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    question_rect = pygame.Rect(0, 0, WIDTH // 1.2, HEIGHT // 1.4)
    question_rect.center = (WIDTH // 2, HEIGHT // 2)

    if manager.chosen_answer == '':
        color = COLORS['GRAY']
        answered = False
    else:
        if manager.question.alt[manager.chosen_answer][3:] == manager.question.answer:
            color = COLORS['GREEN']
            answered = 'right'
            audio.correct.play(loops=1)
        else:
            color = COLORS['DARKRED']
            answered = 'wrong'
            audio.wrong.play()

    surface.fill(BACKGROUND)
    pygame.draw.rect(surface, color, question_rect, 0, 20)
    SCREEN.blit(surface, (0, 0, WIDTH, HEIGHT), (0, 0, WIDTH, HEIGHT))

    SUBFONT = pygame.font.Font('./fonts/dogicapixelbold.ttf', WIDTH // 45)
    question_parts = manager.question.question.split()
    parts = ['']
    for i, value in enumerate(question_parts):
            if len(parts[-1]) < 30:
                parts[-1] += ' ' + value
            else:
                parts.append('')
                parts[-1] += value
    for part in parts:
        draw_title(part, SUBFONT, TITLE_COLOR, surface, color, len(parts) - parts.index(part))

    button_text = [manager.question.alt['a'][3:].rstrip(), manager.question.alt['b'][3:].rstrip(), manager.question.alt['c'][3:].rstrip(), manager.question.alt['d'][3:].rstrip()]
    answer_buttons: list[pygame.Rect] = []
    buttonx = [WIDTH // 7, WIDTH // 1.9]
    buttony = [HEIGHT // 2.4, HEIGHT // 1.6]
    BUTTON_HEIGHT = HEIGHT // 8
    options = ['A) ', 'B) ', 'C) ', 'D) ']

    for i in range(4):
        text_surface = TEXTFONT.render(options[i] + button_text[i], True, BUTTON_TEXTCOLOR)
        text_rect = text_surface.get_rect(center=(buttonx[i % 2] + (BUTTON_WIDTH / 2), buttony[i // 2] + (BUTTON_HEIGHT / 2)))
        rect = pygame.draw.rect(surface, BUTTON_BACKGROUNDCOLOR, (buttonx[i % 2], buttony[i // 2], BUTTON_WIDTH, BUTTON_HEIGHT))
        surface.blit(text_surface, text_rect)
        answer_buttons.append(rect)

    SCREEN.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()

    return answer_buttons, answered


def draw_winners() -> pygame.Rect:
    """
    Displays the top players' history on the SCREEN, including their names, points, and levels,
    along with a back button to return to the previous menu.

    Returns:
    pygame.Rect: A pygame.Rect object representing the back button's position and size.
    """
    back_button = draw_back_button('Histórico')
    ordered_students = get_history()
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)

    players = min(len(ordered_students), 5)
    card_width = MENU_WIDTH
    card_height = MENU_HEIGHT * 0.2
    card_y = HEIGHT - card_width

    for i in range(players):
        player = ordered_students[i]

        pygame.draw.rect(surface, TITLE_COLOR, [MENU_X, ((MENU_Y * 0.8) + (i * 130)), card_width, card_height], 2)

        skin = pygame.image.load(f'img/player/{player.last_skin}.gif')
        skin = pygame.transform.scale(skin, (card_height, card_height))
        skin_rect = skin.get_rect(topleft=(WIDTH / 3.25 - card_height - 30, (card_y * 0.7) + (i * 130) - 8))
        surface.blit(skin, skin_rect)

        text_position = TEXTFONT.render(f'{i + 1}. {player.name}', True, TITLE_COLOR)
        text_rect = text_position.get_rect(topleft=(WIDTH / 3.25, (card_y * 0.7) + (i * 130)))
        surface.blit(text_position, text_rect)

        text_points = TEXTFONT.render(f'Pontuação: {player.points}', True, TITLE_COLOR)
        text_rect = text_points.get_rect(bottomleft=(WIDTH / 3.25, (card_y) + (i * 130)))
        surface.blit(text_points, text_rect)

        text_level = TEXTFONT.render(f'Último labirinto: {player.level}', True, TITLE_COLOR)
        text_rect = text_level.get_rect(bottomleft=(WIDTH / 2, (card_y) + (i * 130)))
        surface.blit(text_level, text_rect)

    SCREEN.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()

    return back_button


def draw_info(info_type:str) -> list[pygame.Rect]:
    buttons = []
    if info_type == 'story':
        back_button = draw_back_button('História')
        buttons.append(back_button)
        continue_button = draw_info_history()
        buttons.append(continue_button)
    else:
        back_button = draw_back_button('Ícones')
        buttons.append(back_button)
        return_button = draw_info_icons()
        buttons.append(return_button)

    pygame.display.flip()
    return buttons

def draw_info_history():
    button_size = FIRST_UNIT // 4
    continue_img = pygame.transform.scale(pygame.image.load('img/arrowRight.png').convert(), (button_size, button_size))
    continue_rect = continue_img.get_rect(topleft=(WIDTH - 2 * button_size, HEIGHT * 0.88))
    SCREEN.blit(continue_img, continue_rect)

    return continue_rect

def draw_info_icons():
    surface = pygame.Surface((SIZE), pygame.SRCALPHA)
    button_size = FIRST_UNIT // 4
    return_img = pygame.transform.scale(pygame.image.load('img/arrowLeft.png').convert(), (button_size, button_size))
    return_rect = return_img.get_rect(topleft=(WIDTH * 0.3, HEIGHT * 0.88))
    card_height = MENU_HEIGHT * 0.2
    card_y = HEIGHT - MENU_WIDTH

    background_rect = pygame.Rect(0, 0, WIDTH // 1.1, HEIGHT // 1.4)
    background_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(surface, FADED_COLOR, background_rect, 0, 20)
    SCREEN.blit(return_img, return_rect)

    card_width = MENU_WIDTH * 2.05
    card_height = card_height / 1.2

    icon_names = ['Coração', 'Bomba', 'Relógio', 'Pontos', 'Fantasma', 'Professor',]
    icons = [HEART, BOMB, CLOCK_ICON, POINT, GHOST, PROF]
    icon_description = ['Representam a quantidade de vida que o jogador tem, e aumenta 1 vida se o jogador estiver sobre ele.',
                        'Este item, ao ser colocado no chão, explode em um área de 3x3. Caso o jogador esteja dentro da área da explosão, ele perderá 1 vida.',
                        'Ao coletar o relógio, 15 segundos são somados ao tempo restante para completar o labirinto.',
                        'Ao coletar este item, o jogador ganha pontos extras.',
                        'Representam alunos que ser perderam no labirinto. Cada um possui uma pergunta, caso o jogador acerte, o aluno é',
                        'libertado e deixa uma recompensa.',
                        'Os professores perseguem jogadores que estão no seu campo de visão. Caso ele chegue perto do jogador, uma pergunta será',
                        'feita e, se a resposta for correta, o professor deixará um item de pontos como recompensa.']

    for i in range(len(icon_names)):
        base_y = i * HEIGHT // 9
        pygame.draw.rect(surface, TITLE_COLOR, [MENU_X // 2.6, ((MENU_Y * 0.8) + base_y), card_width, card_height], 2)

        icon = icons[i]
        icon = pygame.transform.scale(icon, (card_height, card_height))
        icon_rect = icon.get_rect(topleft=(WIDTH / 8.25 - card_height - 20, (card_y * 0.69) + base_y - 8))
        surface.blit(icon, icon_rect)

        text_position = INFOFONT.render(icon_names[i], True, TITLE_COLOR)
        text_rect = text_position.get_rect(topleft=(WIDTH / 8.25, (card_y * 0.69) + base_y))
        surface.blit(text_position, text_rect)

        if i < 4:
            text_points = INFOFONT.render(icon_description[i], True, TITLE_COLOR)
            text_rect = text_points.get_rect(bottomleft=(WIDTH / 8.25, (card_y * 0.91) + base_y))
            surface.blit(text_points, text_rect)
        elif i == 4:
            text_points = INFOFONT.render(icon_description[i], True, TITLE_COLOR)
            text_rect = text_points.get_rect(bottomleft=(WIDTH / 8.25, (card_y * 0.86) + base_y))
            surface.blit(text_points, text_rect)
            text_points = INFOFONT.render(icon_description[i + 1], True, TITLE_COLOR)
            text_rect = text_points.get_rect(bottomleft=(WIDTH / 8.25, (card_y * 0.96) + base_y))
            surface.blit(text_points, text_rect)
        elif i == 5:
            text_points = INFOFONT.render(icon_description[i + 1], True, TITLE_COLOR)
            text_rect = text_points.get_rect(bottomleft=(WIDTH / 8.25, (card_y * 0.86) + base_y))
            surface.blit(text_points, text_rect)
            text_points = INFOFONT.render(icon_description[i + 2], True, TITLE_COLOR)
            text_rect = text_points.get_rect(bottomleft=(WIDTH / 8.25, (card_y * 0.96) + base_y))
            surface.blit(text_points, text_rect)

    SCREEN.blit(surface, (0, 0, WIDTH // 8, HEIGHT // 8), (0, 0, WIDTH, HEIGHT))
    pygame.display.flip()

    return return_rect
