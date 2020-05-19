import glm
import pygame
from OpenGL.GL import *

import game.gui
import game.logic
import game.model.feedback
import game.model.answer
import game.objects3d.sphere
import game.scene
import game.state
from bootstrap.input import Input, Mouse
from bootstrap.events import Events
from bootstrap.camera import Camera

RESOLUTION = (1024, 768)
CAMERA_FRONT = glm.vec3(10.0, 40.0, 15.0)
ANSWERS_START_POS = glm.vec3(0.0, 0.0, 0.0)
ANSWERS_OFFSET = 2.5


class App:
    def __init__(self):
        self.window = pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        self.input = Input(Mouse())
        self.camera = Camera(CAMERA_FRONT)
        self.events = Events()
        self.state = game.state.State()
        self.logic = game.logic.Logic(state=self.state)
        self.gui = game.gui.GUI(show_gui=True)
        self.scene = game.scene.Scene(state=self.state)

        sphere = game.objects3d.sphere.Sphere()

        for row in range(12):
            self.scene.add_child(
                game.model.feedback.Feedback(
                    row,
                    ANSWERS_START_POS,
                    ANSWERS_OFFSET,
                    self.state,
                    sphere
                )
            )
            self.scene.add_child(
                game.model.answer.Answer(
                    row,
                    ANSWERS_START_POS,
                    ANSWERS_OFFSET,
                    self.state,
                    sphere
                )
            )

    def register_events(self):
        mouse = self.input.get_mouse()
        # handle mouse movement
        self.events.on(pygame.MOUSEMOTION, mouse.on_mouse_move)
        # register camera events for movement and zooming
        self.camera.register_event_listeners(self.events, mouse)
        # register SPACEBAR as active selection switcher
        self.events.on(pygame.KEYDOWN, lambda event: self.state.change_selected_index(), conditions={'key': pygame.K_SPACE})
        # check answer after pressing return
        self.events.on(pygame.KEYDOWN, self.logic.check_row, conditions={'key': pygame.K_RETURN})
        # draw scene before gui to avoid transparency issues
        self.events.on(Events.DRAW, self.scene.draw)
        # register gui events
        self.events.on(Events.DRAW, lambda event: self.gui.draw())
        self.events.on(pygame.KEYDOWN, lambda event: self.gui.toggle_visiblity(), conditions={'key': pygame.K_TAB})
        # bind keys 1-6 as selection changers
        keys_to_bind = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        for index, key in enumerate(keys_to_bind):
            self.events.on(
                pygame.KEYDOWN,
                lambda event, data: self.state.set_answer_digit(data['digit']),
                conditions={'key': key},
                data={'digit': index + 1}
            )
        # reset game after pressing R
        self.events.on(pygame.KEYDOWN, lambda event: self.state.reset(), conditions={'key': pygame.K_r})
        # quit the application after clicking X in the window
        self.events.on(pygame.QUIT, lambda event: self.quit())
        # quit the application after pressing ESC key
        self.events.on(pygame.KEYDOWN, lambda event: self.quit(), conditions={'key': pygame.K_ESCAPE})

    def run(self):
        last_frame = 0
        aspect_ratio = RESOLUTION[0] / RESOLUTION[1]

        while True:
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.events.process(pygame.event.get())

            current_frame = pygame.time.get_ticks() / 1000.0
            self.events.post(Events.DRAW, {
                'dt': current_frame - last_frame,
                'resolution': RESOLUTION,
                'camera': self.camera,
                'view': glm.lookAt(self.camera.pos, self.camera.pos + self.camera.front, self.camera.up),
                'projection': glm.perspective(glm.radians(self.camera.zoom), aspect_ratio, 0.1, 100.0)
            })
            last_frame = current_frame

            pygame.display.flip()
            self.clock.tick(60)

    @staticmethod
    def quit():
        pygame.quit()
        quit()


def main():
    pygame.init()

    app = App()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)  # blend is used in GUI texts
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    app.register_events()
    app.run()


if __name__ == '__main__':
    main()
