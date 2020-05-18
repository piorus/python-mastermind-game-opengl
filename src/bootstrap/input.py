import pygame


class Mouse:
    def __init__(self):
        self.first_time = True
        self.last_x = 0.0
        self.last_y = 0.0

        self.x_offset = 0.0
        self.y_offset = 0.0

    def on_mouse_move(self, event):
        if self.first_time:
            self.last_x, self.last_y = pygame.mouse.get_pos()
            self.first_time = False

        x_pos, y_pos = event.pos
        self.x_offset = x_pos - self.last_x
        self.y_offset = self.last_y - y_pos
        self.last_x = x_pos
        self.last_y = y_pos


class Input:
    M_SCROLL_UP = 4
    M_SCROLL_DOWN = 5

    def __init__(self, mouse):
        self.mouse = mouse

    def get_mouse(self):
        return self.mouse
