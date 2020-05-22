class Scene:
    def __init__(self, children: list = None):
        self.children = children if children else []

    def draw(self, event):
        for child in self.children:
            child.draw(event.view, event.projection)

    def add_child(self, child):
        self.children.append(child)
