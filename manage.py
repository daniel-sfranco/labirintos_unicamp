from random import randint
from questions import Question
from animation import Animation
class Manager:
    """
    The `Manager` class is responsible for managing the state and interactions within a game.
    It initializes various attributes related to the game's state, user input, and animations.
    It also generates a random question and initializes an animation sprite.
    """

    def __init__(self):
        """
        Initializes the `Manager` class with default values and sets up the game state, user input, question, and animation.
        """
        self.part = 'init'
        self.running = True
        self.mouse_x = -1
        self.mouse_y = -1
        self.mouse_pressed = False
        self.key_pressed = False
        self.input_active = False
        self.user_input = ""
        self.skin_sel = 0
        self.chosen_answer = ""
        self.questioned = False
        self.num_question = randint(1, 100)
        self.start_pause_time: float = 0
        self.start_question: float = 0
        self.question_giver: tuple[int, int] = (-1, -1)
        self.question_type = ''
        self.question = Question(self.num_question, self.questioned)
        self.bomb_sprite = Animation()
        self.game_number = 0
