""""
This module is used to draw Graphical User Interface on the screen.
It displays game controls.
"""
import pygame

from events import Events
from game.gui_children import Controls, GameResult, ValidationError
from game.state import State
import text
from utils import list_to_str


class Gui:
    """
    GUI class contains logic behind drawing of graphical user interface on the screen.
    It is used to initialize all of the children and wrap some of their functionalities
    in self for a cleaner event handling.
    """

    def __init__(self):
        default_text_shader = text.get_default_shader()

        self.controls = Controls(shader=default_text_shader)

        self.combination_text_object = text.Text(
            'Poprawna kombinacja: -',
            default_text_shader,
            position=(0.0, 0.11),
            font_size=35,
            font_color=(1.0, 1.0, 1.0, 1.0)
        )

        self.game_over = GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='PRZEGRAŁEŚ',
            heading_color=(1.0, 0.0, 0.0, 1.0),
        )

        self.game_won = GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='WYGRAŁEŚ! GRATULACJE.',
            heading_color=(0.0, 1.0, 0.0, 1.0),
        )

        self.cheater = GameResult(
            shader=default_text_shader,
            combination_text_object=self.combination_text_object,
            heading_text='Tere fere.',
            heading_color=(0.0, 1.0, 1.0, 1.0),
        )

        self.validation_error = ValidationError(shader=default_text_shader)

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

    def reset_gui_texts(self, state: State):
        """
        Reset gui texts to consider new state.

        This callback is triggered after EVENTS.AFTER_GAME_RESET event
        and is required to run because combination and game mode
        is changed each time a reset is invoked.

        :param state:
        :return: None
        """
        combination_str = list_to_str(state.combination)
        self.combination_text_object.set_text('Poprawna kombinacja: %s' % combination_str)
        self.cheater.set_heading_text(
            'OSZUST! Złapałeś/łaś mnie!' if state.cheater else 'Tere fere.'
        )

    def on_cheater_check(self):
        """
        Check if cheater.

        :return: None
        """
        self.cheater.show()

    def on_game_won(self):
        """
        Show game won result.

        :return: None
        """
        self.game_won.show()

    def on_game_over(self):
        """
        Show game over result.

        :return: None
        """
        self.game_over.show()

    def show_validation_error(self, validation_text):
        """
        Show validation error.

        :param validation_text: validation error text
        :return:
        """
        # trigger HIDE_VALIDATION_ERROR after 2s to hide it from the screen
        pygame.time.set_timer(Events.HIDE_VALIDATION_ERROR, 2000)
        self.validation_error.set_text(validation_text)
        self.validation_error.show()

    def hide_validation_error(self):
        """
        Hide validation error.

        :return:
        """
        # disable timer
        pygame.time.set_timer(Events.HIDE_VALIDATION_ERROR, 0)
        self.validation_error.hide()
