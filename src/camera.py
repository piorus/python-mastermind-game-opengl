"""camera module"""

import math

import glm
import pygame

from src.events import Events
from src.mouse import Mouse

YAW = -90.0
PITCH = -90.0
SPEED = 25.0
SENSIVITY = 0.3
ZOOM = 45.0
MOVEMENT_BINDINGS = {
    'forward': pygame.K_w,
    'backward': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
}


# pylint: disable=too-many-instance-attributes
class Camera:
    """
    Camera class is used to simulate camera in the game.

    It supports mouse movement and scrolling.
    Camera position can be changed using W, S, A, D keys.
    """

    def __init__(
            self,
            pos=glm.vec3(0.0, 0.0, 0.0),
            up=glm.vec3(0.0, 1.0, 0.0),
            yaw=YAW,
            pitch=PITCH
    ):
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = None
        self.up = None  # pylint: disable=invalid-name

        self.movement_speed = SPEED
        self.mouse_sensivity = SENSIVITY
        self.zoom = ZOOM

        self.pos = pos
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch

        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False

        self.update_camera_vectors()

    def enable_moving(self, direction):
        """
        Enable moving in given direction.

        :param direction: direction that camera should move to
        :return: None
        """
        setattr(self, 'moving_%s' % direction, True)

    def disable_moving(self, direction):
        """
        Disable moving in the given direction.

        :param direction: direction that camera should stop moving to
        :return: None
        """
        setattr(self, 'moving_%s' % direction, False)

    def update_camera_vectors(self):
        """
        Recalculate camera vectors.

        :return: None
        """

        # calculate the new front vector
        front = glm.vec3(
            math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
            math.sin(glm.radians(self.pitch)),
            math.cos(glm.radians(self.pitch)) * math.sin(glm.radians(self.yaw))
        )

        self.front = glm.normalize(front)
        # Also re-calculate the right and up vector
        # normalize the vectors, because their length gets closer to 0
        # the more you look up or down which results in slower movement.
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def register_event_listeners(self, events: Events, mouse: Mouse):
        """
        Register camera listeners for keyboard input, mouse movement and scrolling.

        :param events: Events object
        :param mouse: Mouse object
        :return: None
        """

        # movement bindings
        for direction in ['forward', 'backward', 'left', 'right']:
            events.on(
                pygame.KEYDOWN,
                lambda event, data: self.enable_moving(data['direction']),
                conditions={'key': MOVEMENT_BINDINGS[direction]},
                data={'direction': direction}
            )
            events.on(
                pygame.KEYUP,
                lambda event, data: self.disable_moving(data['direction']),
                conditions={'key': MOVEMENT_BINDINGS[direction]},
                data={'direction': direction}
            )

        # mouse zooming
        events.on(
            pygame.MOUSEBUTTONDOWN,
            lambda event: self.on_scroll_up(),
            conditions={'button': Mouse.M_SCROLL_UP}
        )
        events.on(
            pygame.MOUSEBUTTONDOWN,
            lambda event: self.on_scroll_down(),
            conditions={'button': Mouse.M_SCROLL_DOWN}
        )
        # handle mouse movement
        events.on(
            pygame.MOUSEMOTION,
            lambda event, data: self.on_mouse_movement(data['mouse']),
            data={'mouse': mouse}
        )

        events.on(events.DRAW, self.on_draw)

    def move_forward(self):
        """
        Move camera forward.

        :return: None
        """
        self.pos += self.movement_speed * self.front

    def move_backward(self):
        """
        Move camera backward.

        :return: None
        """
        self.pos -= self.movement_speed * self.front

    def move_left(self):
        """
        Move camera to the left.

        :return: None
        """
        self.pos -= self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def move_right(self):
        """
        Move camera to the right.

        :return: None
        """
        self.pos += self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def on_draw(self, event):
        """
        Callback for the Events.DRAW event that handles camera movement.

        :param event: Events.DRAW event
        :return: None
        """

        self.movement_speed = SPEED * event.dt

        if self.moving_forward:
            self.move_forward()
        if self.moving_backward:
            self.move_backward()
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()

    def on_mouse_movement(self, mouse, constrain_pitch=True):
        """
        Callback for the pygame.MOUSEMOTION event that handles camera movement.

        :param mouse: input.Mouse
        :param constrain_pitch: flag that determine if pitch should be constrained
        :return: None
        """
        self.yaw += (mouse.offset_x * self.mouse_sensivity)
        self.pitch += (mouse.offset_y * self.mouse_sensivity)

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def on_scroll_up(self):
        """
        Callback for the pygame.MOUSEBUTTONDOWN that handles camera zooming up.

        :return: None
        """
        if self.zoom >= 45.0:
            self.zoom = 45.0
        else:
            self.zoom += 5.0

    def on_scroll_down(self):
        """
        Callback for the pygame.MOUSEBUTTONDOWN that handles camera zooming down.

        :return: None
        """
        if self.zoom <= 1.0:
            self.zoom = 1.0
        else:
            self.zoom -= 5.0
