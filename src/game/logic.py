"""logic module"""

from src.game import rules

AVAILABLE_RULES = [
    rules.GameRules,
    rules.CheaterGameRules,
    rules.EnhancedGameRules
]


# pylint: disable=too-few-public-methods
class Logic:
    """
    Logic class is used to handle game logic.
    """

    def __init__(self, state_object):
        self.state = state_object
        self.active_rules = None

    def change_active_rules(self, state_object):
        """
        Change active rules after resetting the game.

        :param state_object: game state
        """
        self.active_rules = self.state.active_rules_class(state_object)

    def check_row(self):
        """
        Check row for the correct answer.
        """
        self.active_rules.check_row()

    def set_answer_digit(self, digit):
        """
        Set answer digit for the currently active cell.

        :param digit: digit to set
        """
        self.active_rules.set_answer_digit(digit)

    def change_active_index(self):
        """
        Change active index of the current row.
        """
        self.active_rules.change_active_index()
