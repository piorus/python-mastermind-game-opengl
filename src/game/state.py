"""state module"""

from random import randint
from typing import List

from src import events


class State:
    """
    State class contains state of the game.

    State properties:
     - answers - 2-dimensional list of answers (12x4)
     - feedback - 2-dimensional list of feedback (12x4)
     - current_row - current row, starts at the end and decrements,
        if game reaches row 0 a game over event is triggered (see game.logic module)
     - active_indices - a list that toggles (using SPACEBAR) which element
        of the current row is selected
     - input_enabled - determines if input is currently enabled
     - cheater - is used to determine which game rules should be used
    """
    combination: List[int]
    answers: List[List[int]]
    feedback: List[List[int]]
    active_indices: List[int]
    current_row: int

    def __init__(self):
        self.combination = [randint(1, 6) for i in range(4)]
        self.answers = [[0 for j in range(4)] for i in range(12)]
        self.feedback = [[] for i in range(12)]
        self.active_indices = [1 if i == 0 else 0 for i in range(4)]
        self.current_row = len(self.answers) - 1
        self.input_enabled = True
        self.cheater = bool(randint(0, 1))

        print('Combination:', self.combination)
        print('Rules:', 'Correct rules enabled.' if not self.cheater else 'CHEATER ENABLED')
        events.post(events.AFTER_GAME_RESET, {'state': self})

    def reset(self):
        """
        Game reset.

        :return: None
        """
        self.__init__()
        events.post(events.GAME_RESET, {})

    def get_active_index(self):
        """
        Return currently activated index.

        :return: currently active index
        """
        return self.active_indices.index(1)

    def change_active_index(self):
        """
        Change active index to the next element.

        In case if no next element is available,
        proceed to the first element.

        :return: None
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

        :param digit: digit to set, this later used to determine color
        :param row: feedback row
        :return: None
        """
        self.feedback[row if row else self.current_row].append(digit)

    def get_answer(self, row):
        """
        Get answer for the given row.

        :param row: answer row
        :return list of the answers for the given row
        """
        return self.answers[row]

    def get_answer_digit(self, row, col):
        """
        Get answer digit for the given row and col.

        :param row: answer row
        :param col: answer col
        :return digit of the answer at given row and col
        :return: None
        """
        return self.get_answer(row)[col]

    def set_answer_digit(self, digit: int, row: int = None, col: int = None):
        """
        Set answer digit for the given row and col.

        :param digit: answer digit
        :param row: answer row
        :param col: answer col
        :return: None
        """
        row = row if row else self.current_row
        col = col if col else self.get_active_index()
        self.answers[row][col] = digit

    def disable_input(self):
        """
        Disable input and wait for the reset.

        :return: None
        """
        self.input_enabled = False
