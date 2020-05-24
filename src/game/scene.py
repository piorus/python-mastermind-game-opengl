"""scene module"""
import glm

import game.opengl_objects
from game.scene_children import Answer, Feedback
from game.state import State

ANSWERS_START_POS = glm.vec3(0.0, 0.0, 0.0)
ANSWERS_OFFSET = 2.5


class Scene:
    """
    Scene class is a container for renderable 3d objects.
    """

    def __init__(self, state: State):
        self.children = []

        sphere = game.opengl_objects.Sphere()

        for row in range(12):
            self.children.append(
                Answer(
                    row,
                    ANSWERS_START_POS,
                    ANSWERS_OFFSET,
                    state,
                    sphere
                )
            )
            self.children.append(
                Feedback(
                    row,
                    ANSWERS_START_POS,
                    ANSWERS_OFFSET,
                    state,
                    sphere
                )
            )

    def draw(self, event):
        """
        Draw scene children on the screen.

        :param event: Events.DRAW event
        :return None
        """
        for child in self.children:
            child.draw(event.view, event.projection, event.camera)

    def add_child(self, child):
        """
        Add scene child.

        :param child: any object that have draw(self, view, projection) method
        :return None
        """
        self.children.append(child)
