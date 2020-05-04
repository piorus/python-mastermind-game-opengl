import glm, math
from pygame.locals import *

class CameraDefaults:
    YAW = -90.0
    PITCH = 0.0
    SPEED = 10.0
    SENSIVITY = 0.3
    ZOOM = 45.0

class Camera:
    def __init__(
        self,
        pos     = glm.vec3(0.0, 0.0, 0.0),
        up      = glm.vec3(0.0, 1.0, 0.0),
        yaw     = CameraDefaults.YAW,
        pitch   = CameraDefaults.PITCH
    ):
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.movement_speed = CameraDefaults.SPEED
        self.mouse_sensivity = CameraDefaults.SENSIVITY
        self.zoom = CameraDefaults.ZOOM

        self.pos = pos
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch

        self.update_camera_vectors()

    def update_camera_vectors(self):
        # calculate the new front vector
        front = glm.vec3(
            math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
            math.sin(glm.radians(self.pitch)),
            math.cos(glm.radians(self.pitch)) * math.sin(glm.radians(self.yaw))
        )

        self.front = glm.normalize(front)
        # Also re-calculate the right and up vector
        self.right = glm.normalize(glm.cross(self.front, self.world_up))  # normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
        self.up    = glm.normalize(glm.cross(self.right, self.front))

    def register_event_listeners(self, input, events):
        input.add_listeners(
            [
                (K_w, self.move_forward, 'Camera::moveForward'),
                (K_s, self.move_backward, 'Camera::moveBackward'),
                (K_a, self.move_left, 'Camera::moveLeft'),
                (K_d, self.move_right, 'Camera::moveRight')
            ]
        )

        events.add_listeners(
            [
                (events.DRAW, self.on_draw, 'Camera::draw'),
                (MOUSEBUTTONDOWN, self.on_mouse_scroll_up, 'Camera::mouseScrollUp', {'button': input.M_SCROLL_UP}),
                (MOUSEBUTTONDOWN, self.on_mouse_scroll_down, 'Camera::mouseScrollDown', {'button': input.M_SCROLL_DOWN})
            ]
        )

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
        self.set_movement_speed(CameraDefaults.SPEED * event.dt)

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        self.yaw    += (x_offset * self.mouse_sensivity)
        self.pitch  += (y_offset * self.mouse_sensivity)

        if(constrain_pitch):
            if(self.pitch > 89.0):
                self.pitch = 89.0
            if(self.pitch < -89.0):
                self.pitch = -89.0

        self.update_camera_vectors()

    def on_mouse_scroll_down(self, event):
        if self.zoom <= 1.0:
            self.zoom = 1.0
        else:
            self.zoom -= 5.0

    def on_mouse_scroll_up(self, event):
        if self.zoom >= 45.0:
            self.zoom = 45.0
        else:
            self.zoom += 5.0
