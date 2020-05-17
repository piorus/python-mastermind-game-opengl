import glm
from game.state import State
from game.objects3d.sphere import Sphere


class Answer:
    ACTIVE_COLOR = glm.vec3(0.0, 1.0, 0.0)
    INACTIVE_COLOR = glm.vec3(1.0, 1.0, 1.0)
    # got colors from: https://www.random.org/colors/hex
    # got normalized values from: http://doc.instantreality.org/tools/color_calculator/
    SELECTION_COLORS = [
        glm.vec3(0.474, 0.847, 0.031),
        glm.vec3(0.752, 0.247, 0.627),
        glm.vec3(0.450, 0.752, 0.768),
        glm.vec3(0.172, 0.333, 0.564),
        glm.vec3(0.635, 0.274, 0.070),
        glm.vec3(1.000, 1.000, 0.000)
    ]

    def __init__(
            self,
            row: int,
            start_pos: glm.vec3,
            offset: float,
            state: State,
            sphere: Sphere
    ):
        self.row = row
        self.start_pos = start_pos
        self.offset = offset
        self.state = state
        self.sphere = sphere

    def draw(
            self,
            view: glm.vec3,
            projection: glm.vec3
    ):
        x_start, y_start, z_start = self.start_pos

        for col in range(4):
            is_selected = self.is_selected(self.row, col)
            answer_x = x_start + col * self.offset
            answer_z = z_start + self.row * self.offset

            model = glm.translate(glm.mat4(1.0), glm.vec3(answer_x, 0.0, answer_z))

            self.sphere.draw(
                model,
                view,
                projection,
                self.get_color(self.row, col, is_selected),
                show_wireframe=is_selected
            )

    def is_selected(self, row: int, col: int):
        return row == self.state.get_current_row() and col == self.state.get_selected_index()

    def get_color(self, row, col, is_selected=False):
        if self.state.get_answer_digit(row, col):
            return Answer.SELECTION_COLORS[self.state.get_answer_digit(row, col) - 1]

        return Answer.ACTIVE_COLOR if is_selected else Answer.INACTIVE_COLOR
