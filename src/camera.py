"""camera module"""

import math

import glm
import pygame

from src import events
from src import mouse

DEFAULT_POSITION = glm.vec3(0.0, 0.0, 0.0)
DEFAULT_UP = glm.vec3(0.0, 1.0, 0.0)
DEFAULT_YAW = -90.0
DEFAULT_PITCH = -90.0
DEFAULT_SPEED = 25.0
DEFAULT_SENSIVITY = 0.3
DEFAULT_ZOOM = 45.0
MOVEMENT_DIRECTIONS = FORWARD, BACKWARD, LEFT, RIGHT = 2, 4, 8, 16
MOVEMENT_BINDINGS = {
    FORWARD: pygame.K_w,
    BACKWARD: pygame.K_s,
    LEFT: pygame.K_a,
    RIGHT: pygame.K_d
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
            position=DEFAULT_POSITION,
            up=DEFAULT_UP,
            yaw=DEFAULT_YAW,
            pitch=DEFAULT_PITCH
    ):
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = None
        self.up = None  # pylint: disable=invalid-name

        self.movement_speed = DEFAULT_SPEED
        self.mouse_sensivity = DEFAULT_SENSIVITY
        self.zoom = DEFAULT_ZOOM

        self.pos = position
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch

        self.movement_direction = 0

        self.update_camera_vectors()

    def enable_moving(self, direction):
        """
        Enable moving in given direction.

        :param direction: direction that camera should move to
        """
        self.movement_direction |= direction

    def disable_moving(self, direction):
        """
        Disable moving in the given direction.

        :param direction: direction that camera should stop moving to
        """
        self.movement_direction ^= direction

    def update_camera_vectors(self):
        """
        Recalculate camera vectors.
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

    def register_event_listeners(self, events_object: events.Events, mouse_object: mouse.Mouse):
        """
        Register camera listeners for keyboard input, mouse movement and scrolling.

        :param events_object: Events object
        :param mouse_object: Mouse object
        """

        # movement bindings
        for direction in MOVEMENT_DIRECTIONS:
            events_object.on(
                pygame.KEYDOWN,
                lambda event, data: self.enable_moving(data['direction']),
                conditions={'key': MOVEMENT_BINDINGS[direction]},
                data={'direction': direction}
            )
            events_object.on(
                pygame.KEYUP,
                lambda event, data: self.disable_moving(data['direction']),
                conditions={'key': MOVEMENT_BINDINGS[direction]},
                data={'direction': direction}
            )

        # mouse zooming
        events_object.on(
            pygame.MOUSEBUTTONDOWN,
            lambda event: self.on_scroll_up(),
            conditions={'button': mouse_object.M_SCROLL_UP}
        )
        events_object.on(
            pygame.MOUSEBUTTONDOWN,
            lambda event: self.on_scroll_down(),
            conditions={'button': mouse_object.M_SCROLL_DOWN}
        )
        # handle mouse movement
        events_object.on(
            pygame.MOUSEMOTION,
            lambda event, data: self.on_mouse_movement(data['mouse']),
            data={'mouse': mouse_object}
        )

        events_object.on(events.DRAW, self.on_draw)

    def move_forward(self):
        """
        Move camera forward.
        """
        self.pos += self.movement_speed * self.front

    def move_backward(self):
        """
        Move camera backward.
        """
        self.pos -= self.movement_speed * self.front

    def move_left(self):
        """
        Move camera to the left.
        """
        self.pos -= self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def move_right(self):
        """
        Move camera to the right.
        """
        self.pos += self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def on_draw(self, event):
        """
        Callback for the Events.DRAW event that handles camera movement.

        :param event: Events.DRAW event
        """

        self.movement_speed = DEFAULT_SPEED * event.dt

        if self.movement_direction & FORWARD:
            self.move_forward()
        if self.movement_direction & BACKWARD:
            self.move_backward()
        if self.movement_direction & LEFT:
            self.move_left()
        if self.movement_direction & RIGHT:
            self.move_right()

    def on_mouse_movement(self, mouse_object: mouse.Mouse, constrain_pitch: bool = True):
        """
        Callback for the pygame.MOUSEMOTION event that handles camera movement.

        :param mouse_object: input.Mouse
        :param constrain_pitch: flag that determine if pitch should be constrained
        """
        self.yaw += (mouse_object.x_offset * self.mouse_sensivity)
        self.pitch += (mouse_object.y_offset * self.mouse_sensivity)

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def on_scroll_up(self):
        """
        Callback for the pygame.MOUSEBUTTONDOWN that handles camera zooming up.
        """
        if self.zoom >= 45.0:
            self.zoom = 45.0
        else:
            self.zoom += 5.0

    def on_scroll_down(self):
        """
        Callback for the pygame.MOUSEBUTTONDOWN that handles camera zooming down.
        """
        if self.zoom <= 1.0:
            self.zoom = 1.0
        else:
            self.zoom -= 5.0
