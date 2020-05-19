from typing import List

class State:
    combination: List[int]
    answers: List[List[int]]
    feedback: List[List[int]]
    selected: List[int]
    current_row: int

    def __init__(self):
        # self.combination = [random.randint(1, 6) for i in range(4)]
        self.combination = [1, 2, 3, 4]
        self.answers = [[0 for j in range(4)] for i in range(12)]
        self.feedback = [[] for i in range(12)]
        self.selected = [1 if i == 0 else 0 for i in range(4)]
        self.current_row = len(self.answers) - 1

        print('combination:', self.combination)

    def reset(self):
        self.__init__()

    def get_combination(self):
        return self.combination

    def get_selected(self):
        return self.selected

    def get_selected_index(self):
        return self.selected.index(1)

    def change_selected_index(self):
        index = self.get_selected_index()
        next_index = 0
        self.selected[index] = 0
        if index + 1 < len(self.selected):
            next_index = index + 1
        self.selected[next_index] = 1

    def get_current_row(self):
        return self.current_row

    def decrement_current_row(self):
        self.current_row -= 1

    def get_feedback(self, row: int):
        return self.feedback[row]

    def get_feedback_digit(self, row: int, col: int):
        return self.get_feedback(row)[col]

    def append_feedback_digit(self, digit: int, row: int = None):
        self.feedback[row if row else self.get_current_row()].append(digit)

    def get_answer(self, row):
        return self.answers[row]

    def get_answer_digit(self, row, col):
        return self.get_answer(row)[col]

    def set_answer_digit(self, digit: int, row: int = None, col: int = None):
        row = row if row else self.get_current_row()
        col = col if col else self.get_selected_index()
        self.answers[row][col] = digit