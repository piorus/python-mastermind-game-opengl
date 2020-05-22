""""
This module is used to draw Graphical User Interface on the screen.
It displays game controls.
"""

import text

DEFAULT_TEXTS = [
    'W, S, A, D - ruch kamerą',
    'SCROLL UP / SCROLL DOWN - przybliżenie / oddalenie',
    '1, 2, 3, 4, 5, 6 - wybór wartości dla danej komórki',
    'SPACJA - zmiana aktywnej komórki',
    'ENTER - sprawdzenie wartości z danego wiersza',
    'R - restart',
    'O - sprawdź czy oszust',  # @TODO implement
    'TAB - pokaż / ukryj GUI',  # @TODO implement
]


class GUI:
    """
    GUI class contains logic behind drawing of graphical user interface on the screen.
    It displays list of strings passed to the constructor
    or DEFAULT_TEXTS in case if no texts are passed.
    It also have a show_gui flag that determines if GUI is visible at the moment.
    """
    def __init__(self, texts: list = None, show_gui: bool = False):
        self.texts = texts if texts else DEFAULT_TEXTS
        self.show_gui = show_gui
        self.text_objects = []

        default_text_shader = text.get_default_shader()

        for index, text_to_draw in enumerate(self.texts):
            self.text_objects.append(
                text.Text(
                    text_to_draw,
                    default_text_shader,
                    position=(0.0, 0.9 - 0.05 * index),
                    font_size=35,
                    font_color=(1.0, 1.0, 0.0, 1.0)
                )
            )

    def toggle_visiblity(self):
        """Toggles GUI visibility"""
        self.show_gui = not self.show_gui

    def draw(self):
        """Draws text lines on the screen"""
        if not self.show_gui:
            return

        for text_object in self.text_objects:
            text_object.draw()
