"""gui_children module contains all of the GUI children."""

import glm

import text

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


class GuiChild:
    """Base class for the GUI child."""

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
    """Controls class is a 'man' of this game. Linux pun intended."""

    def __init__(self, shader):
        super().__init__()

        self.visible = True

        for index, text_to_draw in enumerate(CONTROLS_TEXTS):
            self.children.append(
                text.Text(
                    text_to_draw,
                    shader,
                    position=glm.vec2(0.0, 0.9 - 0.05 * index),
                    font_size=35,
                    font_color=glm.vec4(1.0, 1.0, 0.0, 1.0)
                )
            )


class GameResult(GuiChild):
    """
    GameResult class is used to display results of the following events:
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
            heading_position=(0.0, 0.2),
            heading_color=(1.0, 0.0, 0.0, 1.0),
            heading_font_size=65,
            heading_bg_color=(0.0, 0.0, 0.0, 0.0),
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
                position=(0.0, 0.0),
                font_size=35,
                font_color=(1.0, 1.0, 0.0, 1.0)
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
    """ValidationError class is used to display validation error."""

    def __init__(
            self,
            shader
    ):
        super().__init__()
        self.visible = True
        self.text_object = text.Text(
            '',
            shader,
            position=(0.0, -0.8),
            font_size=35,
            font_color=(1.0, 0.0, 0.0, 1.0)
        )

        self.children.append(self.text_object)

    def set_text(self, validation_text: str):
        """
        Set validation error text.

        :param validation_text: validation text
        :return:
        """
        self.text_object.set_text(validation_text)
