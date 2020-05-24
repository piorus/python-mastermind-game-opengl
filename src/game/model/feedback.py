"""
This module contains Feedback class which is used to render single row of the feedback.

Feedback is only rendered for the checked rows
and feedback rows displayed are equal to the number of checked rows.
(12th feedback row displayed = GAME OVER)
"""

import glm

from game.state import State
from game.opengl_objects.sphere import Sphere


class Feedback:
    """
    Feedback class is used to represent feedback after checking row values.

    Feedback (based on Mastermind rules) depends on multiple of factors:
      - add 1 red sphere for each of the correctly selected answer digit
      - add 1 white sphere for each of the answer digits that are not correctly placed,
        but are in the combination
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            feedback_row: int,
            start_pos: glm.vec3,
            answers_offset: float,
            state: State,
            sphere: Sphere
    ):
        self.row = feedback_row
        self.start_pos = start_pos
        self.answers_offset = answers_offset
        self.feedback_offset = answers_offset / 3
        self.state = state
        self.sphere = sphere

    def draw(self, view: glm.mat4, projection: glm.mat4, camera):
        """
        Draw feedback spheres for the given row on the screen.

        :param view: 4x4 view matrix
        :param projection: 4x4 projection matrix
        """
        for col, feedback_pos in enumerate(self.get_points()):
            if not self.is_visible(col):
                continue

            feedback_x, feedback_z = feedback_pos
            model = glm.translate(glm.mat4(1.0), glm.vec3(feedback_x, 0.0, feedback_z))

            self.sphere.draw(
                model,
                view,
                projection,
                self.get_color(self.row, col),
                camera,
                scale=glm.vec3(0.25, 0.25, 0.25)
            )

    def get_points(self):
        """
        Get position of the feedback digits on the screen.

        This function helps to represent feedback similarly to the board game version.
        :return: list of tuples that contain each of the feedback digit positions
        """
        start_x, start_z = self.start_pos.xz

        x_1 = start_x + 10
        x_2 = x_1 + self.feedback_offset
        z_1 = start_z - self.feedback_offset / 2 + self.row * self.answers_offset
        z_2 = z_1 + self.feedback_offset

        return [(x_1, z_1), (x_2, z_1), (x_1, z_2), (x_2, z_2)]

    def is_visible(self, col: int):
        """
        Check if feedback sphere at given index is visible.

        :param col: index to check
        :return: True/False
        """
        return len(self.state.get_feedback(self.row)) >= col + 1 \
               and self.state.get_feedback_digit(self.row, col) != 0

    def get_color(self, row: int, col: int):
        """
        Get feedback color.

        :param row: feedback row
        :param col: feedback col
        :return: feedback folor
        """
        color = None
        feedback_digit = self.state.get_feedback_digit(row, col)
        if feedback_digit == 1:
            color = glm.vec3(1.0, 0.0, 0.0)
        elif feedback_digit == 2:
            color = glm.vec3(1.0, 1.0, 1.0)

        return color
