import glm
from game.state import State
from game.objects3d.sphere import Sphere


class Feedback:
    def __init__(
            self,
            row: int,
            start_pos: glm.vec3,
            answers_offset: float,
            state: State,
            sphere: Sphere
    ):
        self.row = row
        self.start_pos = start_pos
        self.answers_offset = answers_offset
        self.feedback_offset = answers_offset / 3
        self.state = state
        self.sphere = sphere

    def draw(
            self,
            view: glm.vec3,
            projection: glm.vec3
    ):
        for index, feedback_pos in enumerate(self.get_points()):
            if not self.is_visible(index):
                continue

            feedback_x, feedback_z = feedback_pos
            model = glm.translate(glm.mat4(1.0), glm.vec3(feedback_x, 0.0, feedback_z))
            self.sphere.draw(
                model,
                view,
                projection,
                self.get_color(self.row, index),
                scale=glm.vec3(0.25, 0.25, 0.25)
            )

    def get_points(self):
        x_start, y_start, z_start = self.start_pos

        x1 = x_start + 10
        x2 = x1 + self.feedback_offset
        z1 = z_start - self.feedback_offset / 2 + self.row * self.answers_offset
        z2 = z1 + self.feedback_offset

        return [(x1, z1), (x2, z1), (x1, z2), (x2, z2)]

    def is_visible(self, index):
        return len(self.state.get_feedback(self.row)) >= index + 1 \
               and self.state.get_feedback_digit(self.row, index) != 0

    def get_color(self, row, col):
        color = None
        feedback_digit = self.state.get_feedback_digit(row, col)
        if feedback_digit == 1:
            color = glm.vec3(1.0, 0.0, 0.0)
        elif feedback_digit == 2:
            color = glm.vec3(1.0, 1.0, 1.0)

        return color
