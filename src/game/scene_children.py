"""scene_children module with all of the scene children."""
import glm

from src import camera
from src.game import opengl_objects
from src.game import state

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


# pylint: disable=too-few-public-methods
class SceneChild:
    """Base class for scene child."""

    def draw(self, view: glm.mat4, projection: glm.mat4, camera_object: camera.Camera):
        """Draw child on the screen using view and projection matrices."""


class Answer(SceneChild):
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
            game_state: state.State,
            sphere: opengl_objects.Sphere
    ):
        self.row = answer_row
        self.start_pos = start_pos
        self.offset = offset
        self.state = game_state
        self.sphere = sphere

    def draw(self, view: glm.mat4, projection: glm.mat4, camera_object: camera.Camera):
        """
        Draw answers on the screen using view and projection matrices.

        :param view: 4x4 view matrix
        :param projection: 4x4 projection matrix
        :param camera_object: Camera object
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
                camera_object,
                show_wireframe=is_active
            )

    def is_active(self, row: int, col: int):
        """
        Check if sphere is currently active.

        Activated sphere color can be changed by pressing 1-6.

        :param row: row index of the sphere
        :param col: column index of the sphere
        :return: True or False if selected row is active
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


class Feedback(SceneChild):
    """
    Feedback class is used to represent feedback after checking row values.

    Feedback is only rendered for the checked rows
    and feedback rows displayed are equal to the number of checked rows.
    (12th feedback row displayed = GAME OVER)

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
            game_state: state.State,
            sphere: opengl_objects.Sphere
    ):
        self.row = feedback_row
        self.start_pos = start_pos
        self.answers_offset = answers_offset
        self.feedback_offset = answers_offset / 3
        self.state = game_state
        self.sphere = sphere

    def draw(self, view: glm.mat4, projection: glm.mat4, camera_object: camera.Camera):
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
                camera_object,
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
