"""game rules"""

import collections
from itertools import product
from random import randint

from src import constants
from src import events
from src import utils


def get_row_feedback(answer, combination):
    """
    Get row feedback.
    """
    indices_to_check = []
    feedback = []

    for index, selection in enumerate(answer):
        if combination[index] == selection:
            feedback.append(constants.FEEDBACK_OF_CORRECT_POSITION)
            continue

        indices_to_check.append(index)

    combination_copy = [combination[i] for i in indices_to_check]

    for index in indices_to_check:
        if answer[index] in combination_copy:
            feedback.append(constants.FEEDBACK_OF_WRONG_POSITION)

    return feedback


def game_won(combination: list):
    """
    Post GAME_WON event.
    """
    print(
        'WYGRAŁEŚ. Gratulacje. Poprawna kombinacja: %s'
        % utils.list_to_str(combination)
    )
    events.post(events.GAME_WON, {'combination': combination})


def game_over(combination: list):
    """
    Post GAME_OVER event.
    """
    print('PRZEGRAŁEŚ. Poprawna kombinacja: %s' % utils.list_to_str(combination))
    events.post(events.GAME_OVER, {'combination': combination})


class GameRules:
    """
    GameRules class is handling the game logic in a correct way.
    """

    def __init__(self, state_object):
        self.state = state_object

    def validate_row(self):
        """
        Validate row and post validation errors.
        """
        if 0 in self.state.get_answer():
            print('Błąd. Nie wybrano wszystkich wartości z wiersza.')
            events.post(
                events.SHOW_VALIDATION_ERROR,
                {'validation_text': 'Błąd. Nie wybrano wszystkich wartości z wiersza.'}
            )
            return False

        return True

    def is_won(self):
        """
        Check if game is won.
        """
        return self.state.get_answer() == self.state.combination

    def is_lost(self):
        """
        Check if game is lost.
        """
        return self.state.current_row == 0

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

        if not self.validate_row():
            return

        if self.is_won():
            game_won(self.state.combination)
            return

        self.state.set_row_feedback(
            get_row_feedback(
                self.state.get_answer(),
                self.state.combination
            )
        )

        if self.is_lost():
            game_over(self.state.combination)
            return

        self.state.current_row -= 1

    def set_answer_digit(self, digit):
        """
        Set answer digit.

        :param digit:
        """
        if self.state.input_enabled:
            self.state.set_answer_digit(digit)

    def change_active_index(self):
        """
        Change active index.
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
        """
        if self.state.input_enabled:
            # pure evil
            self.state.set_answer_digit(randint(1, 6))


class EnhancedGameRules(GameRules):
    """
    New game rules. See issue #20
    """
    def __init__(self, state_object):
        super().__init__(state_object)
        self.combinations = [
            [int(digit) for digit in combination]
            for combination in list(product("123456", repeat=constants.COMBINATION_LENGTH))
        ]
        self.counter = collections.Counter()

    def check_row(self):
        if not self.state.input_enabled:
            return

        if not self.validate_row():
            return

        answer = self.state.get_answer()

        for combination in self.combinations:
            feedback = get_row_feedback(answer, combination)
            self.counter[utils.list_to_str(feedback)] += 1

        most_common_feedback = utils.str_to_list(self.counter.most_common(1)[0][0])
        self.state.set_row_feedback(most_common_feedback)
        self.combinations = [
            combination
            for combination in self.combinations
            if get_row_feedback(answer, combination) == most_common_feedback
        ]
        print('combinations:', self.combinations)
        self.counter.clear()

        if len(self.combinations) == 1 and self.state.get_answer() == self.combinations[0]:
            game_won(self.combinations[0])
            return

        if self.state.current_row == 0:
            game_over(self.combinations[0])
            return

        self.state.current_row -= 1
