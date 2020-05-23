import text

TEXTS = [
    'W, S, A, D - ruch kamerą',
    'SCROLL UP / SCROLL DOWN - przybliżenie / oddalenie',
    '1, 2, 3, 4, 5, 6 - wybór wartości dla danej komórki',
    'SPACJA - zmiana aktywnej komórki',
    'ENTER - sprawdzenie wartości z danego wiersza',
    'R - restart',
    'O - sprawdź czy oszust',  # @TODO implement
    'TAB - pokaż / ukryj GUI',
]


class Controls:
    def __init__(self, shader):
        self.texts = TEXTS
        self.visible = True
        self.text_objects = []

        for index, text_to_draw in enumerate(self.texts):
            self.text_objects.append(
                text.Text(
                    text_to_draw,
                    shader,
                    position=(0.0, 0.9 - 0.05 * index),
                    font_size=35,
                    font_color=(1.0, 1.0, 0.0, 1.0)
                )
            )

    def toggle_visiblity(self):
        """Toggles visibility."""
        self.visible = not self.visible

    def draw(self):
        for text_object in self.text_objects:
            text_object.draw()
