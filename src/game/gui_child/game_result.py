import text


class GameResult:
    def __init__(
            self,
            shader,
            heading_text,
            heading_position=(0.0, 0.2),
            heading_color=(1.0, 0.0, 0.0, 1.0),
            heading_font_size=65,
            heading_bg_color=(0.0, 0.0, 0.0, 0.0)
    ):
        self.visible = False
        self.text_objects = []

        self.text_objects.append(
            text.Text(
                heading_text,
                shader,
                position=heading_position,
                font_size=heading_font_size,
                font_color=heading_color,
                bg_color=heading_bg_color
            )
        )

        self.combination_text_object = text.Text(
            'Poprawna kombinacja: -',
            shader,
            position=(0.0, 0.11),
            font_size=35,
            font_color=(1.0, 1.0, 1.0, 1.0)
        )

        self.text_objects.append(self.combination_text_object)

        self.text_objects.append(
            text.Text(
                'Naciśnij R aby spróbować ponownie.',
                shader,
                position=(0.0, 0.0),
                font_size=35,
                font_color=(1.0, 1.0, 0.0, 1.0)
            )
        )

    def set_combination(self, combination: str):
        self.combination_text_object.set_text('Poprawna kombinacja: %s' % combination)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self):
        for text_object in self.text_objects:
            text_object.draw()
