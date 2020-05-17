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
    def __init__(self, texts: list = None, show_gui: bool = False, events: Events = None):
        self.texts = texts if texts else default_texts
        self.show_gui = show_gui
        self.text_objects = []

        self.create_texts_objects()

        if events:
            events.on(events.DRAW, lambda event: [text_object.draw() for text_object in self.text_objects if self.show_gui])
            events.on(pygame.KEYDOWN, lambda event: self.toggle_gui(), conditions={'key': pygame.K_TAB})

    def toggle_gui(self):
        self.show_gui = not self.show_gui

    def create_texts_objects(self):
        text_object_factory = lambda text_to_draw, position: \
            text.Text(
                text_to_draw,
                position=position,
                font_size=35,
                font_color=(1.0, 1.0, 0.0, 1.0)
            )

        for index, text_to_draw in enumerate(self.texts):
            text_object = text_object_factory(text_to_draw, (0.0, 0.9 - 0.05 * index))
            self.text_objects.append(text_object)
