"""state module"""

from typing import List


class State:
    """
    State class represents game state as:
     - 2-dimensional list of answers (12x4)
     - 2-dimensional list of feedback (12x4)
     - current row - at the beginning the last row is selected,
        if game reaches row 0 a game over event is triggered (see game.logic module)
     - active - a list that toggles (using SPACEBAR) which element  of the current row is selected
    """
    combination: List[int]
    answers: List[List[int]]
    feedback: List[List[int]]
    active_indices: List[int]
    current_row: int

    def __init__(self):
        # self.combination = [random.randint(1, 6) for i in range(4)]
        self.combination = [1, 2, 3, 4]
        self.answers = [[0 for j in range(4)] for i in range(12)]
        self.feedback = [[] for i in range(12)]
        self.active_indices = [1 if i == 0 else 0 for i in range(4)]
        self.current_row = len(self.answers) - 1

        print('combination:', self.combination)

    def reset(self):
        """Game reset."""
        self.__init__()

    def get_active_index(self):
        """Return currently activated index."""
        return self.active_indices.index(1)

    def change_active_index(self):
        """
        Change active index to the next element.
        In case if no next element is available,
        proceed to the first element.
        """
        index = self.get_active_index()
        next_index = 0
        self.active_indices[index] = 0
        if index + 1 < len(self.active_indices):
            next_index = index + 1
        self.active_indices[next_index] = 1

    def get_feedback(self, row: int):
        """
        Get list from the feedback row.

        :param row: feedback row
        :return: list with feedback for the row
        """
        return self.feedback[row]

    def get_feedback_digit(self, row: int, col: int):
        """
        Get digit of the feedback for the row at col index.

        :param row: feedback row
        :param col: feedback col
        :return: feedback digit of the row at col index
        """
        return self.get_feedback(row)[col]

    def append_feedback_digit(self, digit: int, row: int = None):
        """
        Append digit to the feedback row.

        In case if no row is passed, current_row is used.

        :param digit: digit to set, this later determine with which color
            a sphere is drawn
        :param row: feedback row
        """
        self.feedback[row if row else self.current_row].append(digit)

    def get_answer(self, row):
        """
        :param row: answer row
        :return list of the answers for the given row
        """
        return self.answers[row]

    def get_answer_digit(self, row, col):
        """
        :param row: answer row
        :param col: answer col
        :return digit of the answer at given row and col
        """
        return self.get_answer(row)[col]

    def set_answer_digit(self, digit: int, row: int = None, col: int = None):
        """
        Set answer digit at the given row and col.

        :param digit: answer digit
        :param row: answer row
        :param col: answer col
        """
        row = row if row else self.current_row
        col = col if col else self.get_active_index()
        self.answers[row][col] = digit
