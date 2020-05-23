"""logic module"""

from game.state import State
from events import Events, post
from utils import combination_to_str


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
            post(
                Events.VALIDATION_ERROR,
                {'message': 'Błąd. Nie wybrano wszystkich wartości z wiersza.'}
            )
            return

        if answer == self.state.combination:
            str_combination = combination_to_str(self.state.combination)
            print('WYGRAŁEŚ. Gratulacje. Poprawna kombinacja: %s' % str_combination)
            post(Events.GAME_WON, {'combination': str_combination})
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
            str_combination = combination_to_str(self.state.combination)
            print('PRZEGRAŁEŚ. Poprawna kombinacja: %s' % str_combination)
            post(Events.GAME_OVER, {'combination': str_combination})
            return

        self.state.current_row -= 1

    def set_answer_digit(self, digit):
        self.state.set_answer_digit(digit)

    def change_active_index(self):
        self.state.change_active_index()
