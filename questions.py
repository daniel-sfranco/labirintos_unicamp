from random import shuffle


class Question:
    def __init__(self, number: int, shuffled: bool) -> None:
        """
        Initialize the Question object by reading the question and answers from the file.

        Args:
            number (int): The question number.
        """
        self.number = number
        with open('questions.che', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        index = self._find_index(lines)
        self._extract_data(lines, index)

    def _find_index(self, lines: list[str]) -> int:
        for i, line in enumerate(lines):
            if line.startswith(str(self.number)) or line.startswith('0' + str(self.number)):
                return i
        return 0

    def _extract_data(self, lines: list[str], index: int) -> None:
        self.question = lines[index].lstrip('.0123456789 ')
        poss =[lines[index + i] for i in range(2, 6)]
        self.alt = {'a': poss[0], 'b': poss[1], 'c': poss[2], 'd': poss[3]}
        self.answer = lines[index + 7][14:]

    def __str__(self) -> str:
        poss = ['a', 'b', 'c', 'd']
        """
        Returns a formatted string representation of the question and its possible answers.

        Returns:
            str: Formatted string with question and answers.
        """
        return f"""Questão {self.number}: {self.question}
{self.alt[poss[0]]}
{self.alt[poss[1]]}
{self.alt[poss[2]]}
{self.alt[poss[3]]}"""


if __name__ == "__main__":
    question = Question(1, False)
