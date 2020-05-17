import pygame
import glm
from OpenGL.GL import *
from bootstrap.input import Input, Mouse, Keyboard
from bootstrap.events import Events
from bootstrap.camera import Camera

resolution = (1024, 768)
camera_front = glm.vec3(10.0, 40.0, 15.0)

pygame.init()
window = pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

mouse = Mouse()
keyboard = Keyboard()

input = Input(mouse, keyboard)
events = Events()

camera = Camera(camera_front)
camera.register_event_listeners(input, events)


def on_mouse_move(event):
    mouse.on_mouse_move(event)
    camera.process_mouse_movement(mouse.x_offset, mouse.y_offset)


events.on(pygame.MOUSEMOTION, on_mouse_move)


def run():
    last_frame = 0
    while True:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        events.process(pygame.event.get())
        input.process(pygame.key.get_pressed())

        current_frame = pygame.time.get_ticks() / 1000.0
        events.post(events.DRAW, {
            'dt': current_frame - last_frame,
            'resolution': resolution,
            'camera': camera,
            'view': glm.lookAt(camera.pos, camera.pos + camera.front, camera.up),
            'projection': glm.perspective(glm.radians(camera.zoom), resolution[0] / resolution[1], 0.1, 100.0)
        })
        last_frame = current_frame

        pygame.display.flip()
        clock.tick(60)
