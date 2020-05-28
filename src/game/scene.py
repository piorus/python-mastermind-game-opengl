"""scene module"""

from src import constants
from src.game import opengl_objects
from src.game import scene_children
from src.game import state


class Scene:
    """
    Scene class is a container for renderable 3d objects.
    """

    def __init__(self, state_object: state.State):
        self.children = []

        sphere = opengl_objects.Sphere()

        for row in range(constants.NUMBER_OF_TRIES):
            self.children.append(
                scene_children.Answer(
                    row,
                    constants.ANSWERS_START_POS,
                    constants.ANSWERS_OFFSET,
                    state_object,
                    sphere
                )
            )
            self.children.append(
                scene_children.Feedback(
                    row,
                    constants.ANSWERS_START_POS,
                    constants.ANSWERS_OFFSET,
                    state_object,
                    sphere
                )
            )

    def draw(self, event):
        """
        Draw scene children on the screen.
        """
        for child in self.children:
            child.draw(event.view, event.projection, event.camera)

    def add_child(self, child):
        """
        Add scene child.

        :param child: any object that have draw(self, view, projection) method
        """
        self.children.append(child)
