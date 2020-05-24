"""
This module contains Answer class which is used to render single row of the answers.
"""

import glm

from game.state import State
from game.opengl_objects.sphere import Sphere

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


class Answer:
    """
    Answer class is used to render 4 colorized spheres representing answers for the given row.

    Colors depend of multiple factors listed below:
      1. white - default color for inactive and unselected answer digit
      2. green - color of the currently active answer digit
            (color selection after pressing 1-6 will apply to this sphere)
      3. Answer.SELECTION_COLORS[0-5] - color of the selected answer digit
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            answer_row: int,
            start_pos: glm.vec3,
            offset: float,
            state: State,
            sphere: Sphere
    ):
        self.row = answer_row
        self.start_pos = start_pos
        self.offset = offset
        self.state = state
        self.sphere = sphere

    def draw(self, view: glm.mat4, projection: glm.mat4, camera):
        """
        Draw answers on the screen using view and projection matrices.

        :param view: 4x4 view matrix
        :param projection: 4x4 projection matrix
        """
        start_x, start_z = self.start_pos.xz

        for col in range(4):
            is_active = self.is_active(self.row, col)
            answer_x = start_x + col * self.offset
            answer_z = start_z + self.row * self.offset

            model = glm.translate(glm.mat4(1.0), glm.vec3(answer_x, 0.0, answer_z))

            self.sphere.draw(
                model,
                view,
                projection,
                self.get_color(self.row, col, is_active),
                camera,
                show_wireframe=is_active
            )

    def is_active(self, row: int, col: int):
        """
        Check if sphere is currently active.

        Activated sphere color can be changed by pressing 1-6.

        :param row: row index of the sphere
        :param col: column index of the sphere
        :return:
        """
        return row == self.state.current_row and col == self.state.get_active_index()

    def get_color(self, row: int, col: int, is_active: bool = False):
        """
        Get color of the sphere.

        :param row: row index of the sphere
        :param col: column index of the sphere
        :param is_active: flag that determine if sphere is currently active
        :return: glm.vec3 vector containing sphere color
        """
        if self.state.get_answer_digit(row, col):
            return SELECTION_COLORS[self.state.get_answer_digit(row, col) - 1]

        return ACTIVE_COLOR if is_active else INACTIVE_COLOR
