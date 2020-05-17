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
        #
        # view = event.view
        # projection = event.projection
        #
        # for row in range(12):
        #
        #     for col in range(4):
        #         is_selected = row == self.state.get_current_row() and col == self.state.get_selected_index()
        #         model = glm.translate(glm.mat4(1.0), glm.vec3(x_start + col * offset, 0.0, z_start + row * offset))
        #         self.sphere.draw(
        #             model,
        #             view,
        #             projection,
        #             self.state.get_color(row, col, is_selected),
        #             show_wireframe=is_selected
        #         )

    def add_child(self, child):
        self.children.append(child)
