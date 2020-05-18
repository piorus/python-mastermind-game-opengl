import pygame
import text
from bootstrap.events import Events

default_texts = [
    'W, S, A, D - ruch kamerą',
    'SCROLL UP / SCROLL DOWN - przybliżenie / oddalenie',
    '1, 2, 3, 4, 5, 6 - wybór wartości dla danej komórki',
    'SPACJA - zmiana aktywnej komórki',
    'ENTER - sprawdzenie wartości z danego wiersza',
    'R - restart',  # @TODO implement
    'O - sprawdź czy oszust',  # @TODO implement
    'TAB - pokaż / ukryj GUI',  # @TODO implement
]


class GUI:
    def __init__(self, texts: list = None, show_gui: bool = False):
        self.texts = texts if texts else default_texts
        self.show_gui = show_gui
        self.text_objects = []

        for index, text_to_draw in enumerate(self.texts):
            self.text_objects.append(
                text.Text(
                    text_to_draw,
                    position=(0.0, 0.9 - 0.05 * index),
                    font_size=35,
                    font_color=(1.0, 1.0, 0.0, 1.0)
                )
            )

    def toggle_visiblity(self):
        self.show_gui = not self.show_gui

    def draw(self):
        if not self.show_gui:
            return

        for text_object in self.text_objects:
            text_object.draw()
