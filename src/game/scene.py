import glm
from bootstrap.events import Events
from game.state import State


class Scene:
    def __init__(
            self,
            events: Events,
            state: State,
            children: list = None
    ):
        self.state = state
        self.children = children if children else []

        events.on(events.DRAW, self.draw)

    def draw(self, event):
        for child in self.children:
            child.draw(event.view, event.projection)

    def add_child(self, child):
        self.children.append(child)
