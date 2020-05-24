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
        self.last_x = 0.0
        self.last_y = 0.0

        self.offset_x = 0.0
        self.offset_y = 0.0

    def on_mouse_move(self, event):
        """
        Callback for the pygame.MOUSEMOTION event that handles mouse movement.

        :param event: pygame Event
        :return: None
        """
        if self.first_time:
            self.last_x, self.last_y = pygame.mouse.get_pos()
            self.first_time = False

        pos_x, pos_y = event.pos
        self.offset_x = pos_x - self.last_x
        self.offset_y = self.last_y - pos_y
        self.last_x = pos_x
        self.last_y = pos_y
