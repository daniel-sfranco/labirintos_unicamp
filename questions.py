class Question:
    def __init__(self, number):
        self.number = number
        with open('questions.che', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(str(number)):
                    n = number
                    i = 0
                    while n > 0:
                        n //= 10
                        i += 1
                    self.question = line.strip()[i+1:]
                    index = lines.index(line)
            self.a = lines[index+2].strip()
            self.b = lines[index+3].strip()
            self.c = lines[index+4].strip()
            self.d = lines[index+5].strip()
            self.answer = lines[index+7][11]
    def __str__(self):
        return f"""Questão {self.number}: {self.question}
{self.a}
{self.b}
{self.c}
{self.d}"""

if __name__ == "__main__":
    num = int(input())
    question = Question(num)
    print(question)
    selected = input("Your answer: ")
    if selected.lower()[0] == question.answer.lower()[0]:
        print("Correct!")
    else:
        print("Incorrect!")