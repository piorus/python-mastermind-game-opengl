import glm, math
import pygame

from bootstrap.input import Mouse

YAW = -90.0
PITCH = -90.0
SPEED = 25.0
SENSIVITY = 0.3
ZOOM = 45.0

class Camera:
    def __init__(
            self,
            pos=glm.vec3(0.0, 0.0, 0.0),
            up=glm.vec3(0.0, 1.0, 0.0),
            yaw=YAW,
            pitch=PITCH
    ):
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = None
        self.up = None

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
        setattr(self, 'moving_%s' % direction, True)

    def disable_moving(self, direction):
        setattr(self, 'moving_%s' % direction, False)

    def update_camera_vectors(self):
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

    def register_event_listeners(self, events, mouse):
        # movement bindings
        events.on(pygame.KEYDOWN, lambda event: self.enable_moving('forward'), conditions={'key': pygame.K_w})
        events.on(pygame.KEYDOWN, lambda event: self.enable_moving('backward'), conditions={'key': pygame.K_s})
        events.on(pygame.KEYDOWN, lambda event: self.enable_moving('left'), conditions={'key': pygame.K_a})
        events.on(pygame.KEYDOWN, lambda event: self.enable_moving('right'), conditions={'key': pygame.K_d})

        events.on(pygame.KEYUP, lambda event: self.disable_moving('forward'), conditions={'key': pygame.K_w})
        events.on(pygame.KEYUP, lambda event: self.disable_moving('backward'), conditions={'key': pygame.K_s})
        events.on(pygame.KEYUP, lambda event: self.disable_moving('left'), conditions={'key': pygame.K_a})
        events.on(pygame.KEYUP, lambda event: self.disable_moving('right'), conditions={'key': pygame.K_d})
        # mouse zooming
        events.on(pygame.MOUSEBUTTONDOWN, lambda event: self.scroll_up(), conditions={'button': Mouse.M_SCROLL_UP})
        events.on(pygame.MOUSEBUTTONDOWN, lambda event: self.scroll_down(), conditions={'button': Mouse.M_SCROLL_DOWN})
        # handle mouse movement
        events.on(pygame.MOUSEMOTION, lambda event, data: self.mouse_movement(data['mouse']), data={'mouse': mouse})

        events.on(events.DRAW, self.on_draw)

    def move_forward(self):
        self.pos += self.movement_speed * self.front

    def move_backward(self):
        self.pos -= self.movement_speed * self.front

    def move_left(self):
        self.pos -= self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def move_right(self):
        self.pos += self.movement_speed * glm.normalize(glm.cross(self.front, self.up))

    def set_movement_speed(self, movement_speed):
        self.movement_speed = movement_speed

    def set_front(self, front):
        self.front = front

    def on_draw(self, event):
        self.set_movement_speed(SPEED * event.dt)

        if self.moving_forward: self.move_forward()
        if self.moving_backward: self.move_backward()
        if self.moving_left: self.move_left()
        if self.moving_right: self.move_right()

    def mouse_movement(self, mouse, constrain_pitch=True):
        self.yaw += (mouse.x_offset * self.mouse_sensivity)
        self.pitch += (mouse.y_offset * self.mouse_sensivity)

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def scroll_down(self):
        if self.zoom <= 1.0:
            self.zoom = 1.0
        else:
            self.zoom -= 5.0

    def scroll_up(self):
        if self.zoom >= 45.0:
            self.zoom = 45.0
        else:
            self.zoom += 5.0
