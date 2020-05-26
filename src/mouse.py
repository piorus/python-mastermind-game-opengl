"""input module"""

import pygame


# pylint: disable=too-few-public-methods
class Mouse:
    """
    Mouse class is used to handle mouse input in the game.
    """

    M_SCROLL_UP = 4
    M_SCROLL_DOWN = 5

    def __init__(self):
        self.first_time = True
        self.x_last = 0.0
        self.y_last = 0.0

        self.x_offset = 0.0
        self.y_offset = 0.0

    def on_mouse_move(self, event):
        """
        Callback for the pygame.MOUSEMOTION event that handles mouse movement.

        :param event: pygame Event
        """
        if self.first_time:
            self.x_last, self.y_last = pygame.mouse.get_pos()
            self.first_time = False

        x_pos, y_pos = event.pos
        self.x_offset = x_pos - self.x_last
        self.y_offset = self.y_last - y_pos
        self.x_last = x_pos
        self.y_last = y_pos
