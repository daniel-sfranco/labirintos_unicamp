from random import randint
from questions import Question
from animation import Animation
class Manager:
    def __init__(self):
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
        self.question = Question(self.num_question)
        self.bomb_sprite = Animation()