from random import randint
class Teacher:
    def __init__(self, game) -> None:
        while True:
            self.coordinate = [randint(0, len(game.maze)) - 1, randint(0, len(game.maze[0]) - 1)]
            if self.coordinate == [len(game.maze) - 1, len(game.maze[0]) - 1]:
                continue
            elif game.maze[self.coordinate[0]][self.coordinate[1]] != 0:
                continue
            else:
                break

def set_teachers(game):
    teachers = []
    for _ in range(game.level):
        teachers.append(Teacher(game))
    return teachers