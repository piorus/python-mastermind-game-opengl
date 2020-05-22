"""logic module"""

from game.state import State


# pylint: disable=too-few-public-methods
class Logic:
    """Logic class is used to handle game logic."""

    def __init__(self, state: State):
        self.state = state

    def check_row(self):
        """
        This function is checking answers for the current row,
        triggers win and game over events.

        In case if game is not won or not over, a feedback is generated
        for the answered combination.
        """
        current_row = self.state.current_row
        answer = self.state.get_answer(current_row)
        if 0 in answer:
            print('Błąd. Nie wybrano wszystkich wartości z wiersza.')
            # @TODO trigger validation error
            return

        if answer == self.state.combination:
            print('YOU WIN. Congratulations.')
            # @TODO trigger game end event
            return

        indices_to_check = []
        combination = self.state.combination

        for index, selection in enumerate(answer):
            if combination[index] == selection:
                self.state.append_feedback_digit(1)
                continue

            indices_to_check.append(index)

        combination_copy = [combination[i] for i in indices_to_check]

        for index in indices_to_check:
            if answer[index] in combination_copy:
                self.state.append_feedback_digit(2)

        if current_row == 0:
            print('Game over.')
            # @TODO trigger gameover event
            return

        self.state.current_row -= 1
