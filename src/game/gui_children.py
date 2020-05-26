"""gui_children module contains all of the GUI children."""

import glm

from src import text

CONTROLS_TEXTS = [
    'W, S, A, D - ruch kamerą',
    'SCROLL UP / SCROLL DOWN - przybliżenie / oddalenie',
    '1, 2, 3, 4, 5, 6 - wybór wartości dla danej komórki',
    'SPACJA - zmiana aktywnej komórki',
    'ENTER - sprawdzenie wartości z danego wiersza',
    'R - restart',
    'O - sprawdź czy oszust',
    'TAB - pokaż / ukryj GUI',
]

DEFAULT_CONTROLS_COLOR = glm.vec4(1.0, 1.0, 0.0, 1.0)
DEFAULT_CONTROLS_FONT_SIZE = 35

DEFAULT_HEADING_POSITION = glm.vec2(0.0, 0.2)
DEFAULT_HEADING_COLOR = glm.vec4(1.0, 0.0, 0.0, 1.0)
DEFAULT_HEADING_FONT_SIZE = 65
DEFAULT_HEADING_BACKGROUND_COLOR = glm.vec4(0.0, 0.0, 0.0, 0.0)

DEFAULT_RESTART_POSITION = glm.vec2(0.0, 0.0)
DEFAULT_RESTART_COLOR = glm.vec4(1.0, 1.0, 0.0, 1.0)
DEFAULT_RESTART_FONT_SIZE = 35

DEFAULT_VALIDATION_ERROR_POSITION = glm.vec2(0.0, -0.8)
DEFAULT_VALIDATION_ERROR_FONT_COLOR = glm.vec4(1.0, 0.0, 0.0, 1.0)
DEFAULT_VALIDATION_ERROR_FONT_SIZE = 35

class GuiChild:
    """
    Base class for the GUI child.
    """

    def __init__(self):
        self.visible = False
        self.children = []

    def draw(self):
        """
        Draw GUI child.

        :return: None
        """
        for child in self.children:
            child.draw()

    def toggle_visiblity(self):
        """
        Toggles visibility.

        :return: None
        """
        self.visible = not self.visible

    def show(self):
        """
        Turn visiblity on.

        :return: None
        """
        self.visible = True

    def hide(self):
        """
        Turn visibility off.

        :return: None
        """
        self.visible = False


class Controls(GuiChild):
    """
    Controls class is a 'man' of this game. Linux pun intended.
    """

    def __init__(self, shader):
        super().__init__()

        self.visible = True

        for index, text_to_draw in enumerate(CONTROLS_TEXTS):
            self.children.append(
                text.Text(
                    text_to_draw,
                    shader,
                    position=glm.vec2(0.0, 0.9 - 0.05 * index),
                    font_color=DEFAULT_CONTROLS_COLOR,
                    font_size=DEFAULT_CONTROLS_FONT_SIZE
                )
            )


class GameResult(GuiChild):
    """
    GameResult class is used to display game result.

    Supported game results are:
    - game over
    - game won
    - cheater check
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            shader,
            combination_text_object: text.Text,
            heading_text,
            heading_position=DEFAULT_HEADING_POSITION,
            heading_color=DEFAULT_HEADING_COLOR,
            heading_font_size=DEFAULT_HEADING_FONT_SIZE,
            heading_bg_color=DEFAULT_HEADING_BACKGROUND_COLOR,
    ):
        super().__init__()

        self.heading = text.Text(
            heading_text,
            shader,
            position=heading_position,
            font_size=heading_font_size,
            font_color=heading_color,
            bg_color=heading_bg_color
        )
        self.children.append(self.heading)
        self.children.append(combination_text_object)

        self.children.append(
            text.Text(
                'Naciśnij R aby spróbować ponownie.',
                shader,
                position=DEFAULT_RESTART_POSITION,
                font_color=DEFAULT_RESTART_COLOR,
                font_size=DEFAULT_RESTART_FONT_SIZE
            )
        )

    def set_heading_text(self, heading_text: str):
        """
        Set heading text.

        :param heading_text: heading text
        :return: None
        """
        self.heading.set_text(heading_text)


class ValidationError(GuiChild):
    """
    ValidationError class is used to display validation error.
    """

    def __init__(
            self,
            shader
    ):
        super().__init__()
        self.visible = True
        self.text_object = text.Text(
            '',
            shader,
            position=DEFAULT_VALIDATION_ERROR_POSITION,
            font_color=DEFAULT_VALIDATION_ERROR_FONT_COLOR,
            font_size=DEFAULT_VALIDATION_ERROR_FONT_SIZE
        )

        self.children.append(self.text_object)

    def set_text(self, validation_text: str):
        """
        Set validation error text.

        :param validation_text: validation text
        :return: None
        """
        self.text_object.set_text(validation_text)
