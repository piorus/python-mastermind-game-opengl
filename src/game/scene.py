"""scene module"""


class Scene:
    """
    Scene class is a container for renderable 3d objects.
    """

    def __init__(self, children: list = None):
        self.children = children if children else []

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
