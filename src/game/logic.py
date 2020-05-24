"""logic module"""
from random import randint

from game.state import State
from events import Events, post
from utils import list_to_str


class GameRules:
    def __init__(self, state):
        self.state = state

    def check_row(self):
        """
        This function is checking answers for the current row,
        triggers win and game over events.

        In case if game is not won or not over, a feedback is generated
        for the answered combination.
        """
        if not self.state.input_enabled:
            return

        current_row = self.state.current_row
        answer = self.state.get_answer(current_row)
        combination = self.state.combination

        if 0 in answer:
            print('Błąd. Nie wybrano wszystkich wartości z wiersza.')
            post(
                Events.VALIDATION_ERROR,
                {'message': 'Błąd. Nie wybrano wszystkich wartości z wiersza.'}
            )
            return

        if answer == combination:
            str_combination = list_to_str(self.state.combination)
            print('WYGRAŁEŚ. Gratulacje. Poprawna kombinacja: %s' % str_combination)
            post(Events.GAME_WON, {'combination': str_combination})
            return

        indices_to_check = []

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
            str_combination = list_to_str(self.state.combination)
            print('PRZEGRAŁEŚ. Poprawna kombinacja: %s' % str_combination)
            post(Events.GAME_OVER, {'combination': str_combination})
            return

        self.state.current_row -= 1

    def set_answer_digit(self, digit):
        if self.state.input_enabled:
            self.state.set_answer_digit(digit)

    def change_active_index(self):
        if self.state.input_enabled:
            self.state.change_active_index()


class CheaterGameRules(GameRules):
    def __init__(self, state):
        super().__init__(state)

    def set_answer_digit(self, digit):
        if self.state.input_enabled:
            # pure evil
            self.state.set_answer_digit(randint(0, 6))


# pylint: disable=too-few-public-methods
class Logic:
    """Logic class is used to handle game logic."""

    def __init__(self, state: State):
        self.state = state
        self.rules = GameRules(state)
        self.cheater_rules = CheaterGameRules(state)

    def check_row(self):
        if self.state.cheater:
            self.cheater_rules.check_row()
        else:
            self.rules.check_row()

    def set_answer_digit(self, digit):
        if self.state.cheater:
            self.cheater_rules.set_answer_digit(digit)
        else:
            self.rules.set_answer_digit(digit)

    def change_active_index(self):
        if self.state.cheater:
            self.cheater_rules.change_active_index()
        else:
            self.rules.change_active_index()
