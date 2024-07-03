class Question:
    def __init__(self, number):
        self.number = number
        with open('questions.che', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(str(self.number)) or line.startswith('0' + str(self.number)):
                    index = lines.index(line)
                    break
        self.question = lines[index]
        while self.question.startswith('.') or self.question[0].isnumeric() or self.question.startswith(' '):
            self.question = self.question[1:]
        self.a = lines[index + 2].strip()
        self.b = lines[index + 3].strip()
        self.c = lines[index + 4].strip()
        self.d = lines[index + 5].strip()
        self.answer = lines[index + 7][11]

    def __str__(self):
        return f"""Questão {self.number}: {self.question}
{self.a}
{self.b}
{self.c}
{self.d}"""


if __name__ == "__main__":
    num = int(input())
    question = Question(num)
    selected = input("Your answer: ")
    if selected.lower()[0] == question.answer.lower()[0]:
        print("Correct!")
    else:
        print("Incorrect!")
