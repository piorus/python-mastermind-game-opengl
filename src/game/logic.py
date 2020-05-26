"""logic module"""
from random import randint

from src import events
from src import utils
from src.game import state


class GameRules:
    """
    GameRules class is handling the game logic in a correct way.
    """

    def __init__(self, state: state.State):
        self.state = state

    def check_row(self):
        """
        Check answer for the current row.

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
            events.post(
                events.Events.SHOW_VALIDATION_ERROR,
                {'validation_text': 'Błąd. Nie wybrano wszystkich wartości z wiersza.'}
            )
            return

        if answer == combination:
            print(
                'WYGRAŁEŚ. Gratulacje. Poprawna kombinacja: %s'
                % utils.list_to_str(self.state.combination)
            )
            events.post(events.Events.GAME_WON, {})
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
            print('PRZEGRAŁEŚ. Poprawna kombinacja: %s' % utils.list_to_str(self.state.combination))
            events.post(events.Events.GAME_OVER, {})
            return

        self.state.current_row -= 1

    def set_answer_digit(self, digit):
        """
        Set answer digit.

        :param digit:
        :return: None
        """
        if self.state.input_enabled:
            self.state.set_answer_digit(digit)

    def change_active_index(self):
        """
        Change active index.

        :return: None
        """
        if self.state.input_enabled:
            self.state.change_active_index()


class CheaterGameRules(GameRules):
    """
    CheaterGameRules class is handling the game logic in a wrong way.
    """

    def set_answer_digit(self, digit):
        """
        Incorrectly sets answer digit using random integer.

        :param digit: digit to set, randomint is used instead of this parameter
        :return: None
        """
        if self.state.input_enabled:
            # pure evil
            self.state.set_answer_digit(randint(1, 6))


# pylint: disable=too-few-public-methods
class Logic:
    """
    Logic class is used to handle game logic.
    """

    def __init__(self, state: state.State):
        self.state = state
        self.rules = GameRules(state)
        self.cheater_rules = CheaterGameRules(state)
        self.active_rules = None

    def change_active_rules(self, state: state.State):
        """
        Change active rules after resetting the game.

        :param state: game state
        :return: None
        """
        self.active_rules = self.cheater_rules if state.cheater else self.rules

    def check_row(self):
        """
        Check row for the correct answer.

        :return: None
        """
        self.active_rules.check_row()

    def set_answer_digit(self, digit):
        """
        Set answer digit for the currently active cell.

        :param digit: digit to set
        :return: None
        """
        self.active_rules.set_answer_digit(digit)

    def change_active_index(self):
        """
        Change active index of the current row.

        :return: None
        """
        self.active_rules.change_active_index()
