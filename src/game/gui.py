""""
This module is used to draw Graphical User Interface on the screen.
It displays game controls.
"""
import glm
import pygame

from src import constants
from src import events
from src import text
from src import utils
from src.game import gui_children
from src.game import state

DEFAULT_COMBINATION_TEXT_POSITION = glm.vec2(0.0, 0.11)
DEFAULT_COMBINATION_TEXT_FONT_SIZE = 35


class Gui:
    """
    Gui class is used to render graphical user interface.

    It initializes all of the children and wrap some of their functionalities
    in self for a cleaner event handling.
    """

    def __init__(self):
        default_text_shader = text.get_default_shader()

        self.controls = gui_children.Controls(shader=default_text_shader)

        self.combination_text_object = text.Text(
            'Poprawna kombinacja: -',
            default_text_shader,
            position=DEFAULT_COMBINATION_TEXT_POSITION,
            font_size=DEFAULT_COMBINATION_TEXT_FONT_SIZE,
            font_color=constants.COLOR_WHITE
        )

        self.game_over = gui_children.GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='PRZEGRAŁEŚ',
            heading_color=constants.COLOR_RED,
        )

        self.game_won = gui_children.GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='WYGRAŁEŚ! GRATULACJE.',
            heading_color=constants.COLOR_GREEN,
        )

        self.cheater = gui_children.GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='Tere fere.',
            heading_color=constants.COLOR_LIGHT_BLUE,
        )

        self.validation_error = gui_children.ValidationError(shader=default_text_shader)

        self.children = [
            self.game_won,
            self.game_over,
            self.controls,
            self.cheater,
            self.validation_error
        ]

    def draw(self):
        """
        Draw visible children.

        :return: None
        """
        for child in self.children:
            if child.visible:
                child.draw()

    def toggle_controls_visibility(self):
        """
        Toggle controls visibility.

        :return: None
        """
        self.controls.toggle_visiblity()

    def hide_result(self):
        """
        Hide any visible result.

        :return: None
        """
        if self.game_over.visible:
            self.game_over.hide()
        if self.game_won.visible:
            self.game_won.hide()
        if self.cheater.visible:
            self.cheater.hide()

    def reset_gui_texts(self, state_object: state.State):
        """
        Reset gui texts to consider new state.

        This callback is triggered after EVENTS.AFTER_GAME_RESET event
        and is required to run because combination and game mode
        is changed each time a reset is invoked.

        :param state_object: State object
        :return: None
        """
        print(state_object.active_rules_class)
        combination_str = utils.list_to_str(state_object.combination)
        self.combination_text_object.set_text('Poprawna kombinacja: %s' % combination_str)
        self.cheater.set_heading_text(
            'OSZUST! Złapałeś/łaś mnie!'
            if str(state_object.active_rules_class) == "<class 'src.game.rules.CheaterGameRules'>"
            else 'Tere fere.'
        )

    def on_cheater_check(self):
        """
        Check if cheater.

        :return: None
        """
        self.cheater.show()

    def on_game_won(self, combination: list):
        """
        Show game won result.

        :return: None
        """
        self.combination_text_object.set_text(
            'Poprawna kombinacja: %s' % utils.list_to_str(combination)
        )
        self.game_won.show()

    def on_game_over(self, combination: list):
        """
        Show game over result.

        :return: None
        """
        self.combination_text_object.set_text(
            'Poprawna kombinacja: %s' % utils.list_to_str(combination)
        )
        self.game_over.show()

    def show_validation_error(self, validation_text: str):
        """
        Show validation error.

        :param validation_text: validation error text
        :return:
        """
        # trigger HIDE_VALIDATION_ERROR after 2s to hide it from the screen
        pygame.time.set_timer(events.HIDE_VALIDATION_ERROR, 2000)
        self.validation_error.set_text(validation_text)
        self.validation_error.show()

    def hide_validation_error(self):
        """
        Hide validation error.

        :return:
        """
        # disable timer
        pygame.time.set_timer(events.HIDE_VALIDATION_ERROR, 0)
        self.validation_error.hide()
