""""
This module is used to draw Graphical User Interface on the screen.
It displays game controls.
"""

import text
from game.gui_child.controls import Controls
from game.gui_child.game_result import GameResult


class Gui:
    """
    GUI class contains logic behind drawing of graphical user interface on the screen.
    It displays list of strings passed to the constructor
    or DEFAULT_TEXTS in case if no texts are passed.
    It also have a show_gui flag that determines if GUI is visible at the moment.
    """

    def __init__(self):
        default_text_shader = text.get_default_shader()

        self.controls = Controls(shader=default_text_shader)

        self.game_over = GameResult(
            shader=default_text_shader,
            heading_text='PRZEGRAŁEŚ',
            heading_color=(1.0, 0.0, 0.0, 1.0),
        )

        self.game_won = GameResult(
            shader=default_text_shader,
            heading_text='WYGRAŁEŚ! GRATULACJE.',
            heading_color=(0.0, 1.0, 0.0, 1.0),
        )

        self.children = [self.game_over, self.game_won, self.controls]

    def draw(self):
        """Draws text lines on the screen"""
        for child in self.children:
            if child.visible:
                child.draw()

    def toggle_controls_visibility(self):
        self.controls.toggle_visiblity()

    def hide_results(self):
        if self.game_over.visible:
            self.game_over.hide()
        if self.game_won.visible:
            self.game_won.hide()

    def on_game_won(self, combination):
        self.game_won.set_combination(combination)
        self.game_won.show()

    def on_game_over(self, combination):
        self.game_over.set_combination(combination)
        self.game_over.show()
