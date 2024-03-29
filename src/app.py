"""
Main project file.
It contains App class that create most of the game objects
and register game events.
This is the place where main game loop is located (run() method).
"""
import sys

import glm
from OpenGL import GL
import pygame

from src import camera
from src import mouse
from src import events
from src.game import state
from src.game import gui
from src.game import logic
from src.game import scene

RESOLUTION = (1024, 768)
WINDOW_CAPTION = 'Piotr Rusin - Projekt zaliczeniowy z Języków Symbolicznych (rok 2020)'
CAMERA_FRONT = glm.vec3(10.0, 40.0, 15.0)


# pylint: disable=too-many-instance-attributes
class App:
    """
    Core of the game application.

    This class creates most of the game objects and
    handles event listeners registration.
    It also contains the main game loop.
    """

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.mouse = mouse.Mouse()
        self.camera = camera.Camera(CAMERA_FRONT)
        self.events = events.Events()
        self.state = state.State()
        self.logic = logic.Logic(state_object=self.state)
        self.gui = gui.Gui()
        self.scene = scene.Scene(state_object=self.state)

    def register_events(self):
        """
        Register event listeners used in the application.
        """
        # handle mouse movement
        self.events.on(pygame.MOUSEMOTION, self.mouse.on_mouse_move)
        # register camera events for movement and zooming
        self.camera.register_event_listeners(self.events, self.mouse)
        # register SPACEBAR as active selection switcher
        self.events.on(
            pygame.KEYDOWN,
            lambda event: self.logic.change_active_index(),
            conditions={'key': pygame.K_SPACE}
        )
        # check answer after pressing return
        self.events.on(
            pygame.KEYDOWN,
            lambda event: self.logic.check_row(),
            conditions={'key': pygame.K_RETURN}
        )
        # draw scene before gui to avoid transparency issues
        self.events.on(events.DRAW, self.scene.draw)
        # toggle controls texts visibility
        self.events.on(
            pygame.KEYDOWN,
            lambda event: self.gui.toggle_controls_visibility(),
            conditions={'key': pygame.K_TAB}
        )
        # draw gui
        self.events.on(events.DRAW, lambda event: self.gui.draw())
        # bind keys 1-6 as selection changers
        keys_to_bind = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
        for index, key in enumerate(keys_to_bind):
            self.events.on(
                pygame.KEYDOWN,
                lambda event, data: self.logic.set_answer_digit(data['digit']),
                conditions={'key': key},
                data={'digit': index + 1}
            )

        # check if cheater after pressing O
        self.events.on(
            pygame.KEYDOWN,
            lambda event: events.post(events.CHEATER_CHECK, {'state': self.state}),
            conditions={'key': pygame.K_o}
        )
        # show text with result of the check
        self.events.on(events.CHEATER_CHECK, lambda event: self.gui.on_cheater_check())
        # disable input, wait for reset
        self.events.on(events.CHEATER_CHECK, lambda event: self.state.disable_input())

        # reset game after pressing R
        self.events.on(
            pygame.KEYDOWN,
            lambda event: events.post(events.GAME_RESET, {}),
            conditions={'key': pygame.K_r}
        )
        self.events.on(
            events.GAME_RESET,
            lambda event: self.state.reset()
        )
        # change game results texts to the new combination after resetting the game
        self.events.on(
            events.AFTER_GAME_RESET,
            lambda event: self.gui.reset_gui_texts(event.state)
        )
        # hide previous game result after resetting the game
        self.events.on(events.AFTER_GAME_RESET, lambda event: self.gui.hide_result())
        # show result message and disable input when the game is won
        self.events.on(events.GAME_WON, lambda event: self.gui.on_game_won(event.combination))
        # disable input, wait for reset
        self.events.on(events.GAME_WON, lambda event: self.state.disable_input())
        # show result message and disable input when the game is lost
        self.events.on(events.GAME_OVER, lambda event: self.gui.on_game_over(event.combination))
        # disable input, wait for reset
        self.events.on(events.GAME_OVER, lambda event: self.state.disable_input())
        # show validation error
        self.events.on(
            events.SHOW_VALIDATION_ERROR,
            lambda event: self.gui.show_validation_error(event.validation_text)
        )
        # hide validation error
        self.events.on(
            events.HIDE_VALIDATION_ERROR,
            lambda event: self.gui.hide_validation_error()
        )
        # set active rules for the current game (depends on the11 cheater state)
        self.events.on(
            events.AFTER_GAME_RESET,
            lambda event: self.logic.change_active_rules(self.state)
        )
        # quit the application after clicking X in the window
        self.events.on(pygame.QUIT, lambda event: self.quit())
        # quit the application after pressing ESC key
        self.events.on(
            pygame.KEYDOWN,
            lambda event: self.quit(),
            conditions={'key': pygame.K_ESCAPE}
        )

    def run(self):
        """
        Main game loop.
        """

        last_frame = 0
        aspect_ratio = RESOLUTION[0] / RESOLUTION[1]

        while True:
            GL.glClearColor(0.0, 0.0, 0.0, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.events.process(pygame.event.get())

            current_frame = pygame.time.get_ticks() / 1000.0
            events.post(
                events.DRAW,
                {
                    'dt': current_frame - last_frame,
                    'resolution': RESOLUTION,
                    'camera': self.camera,
                    'view': glm.lookAt(
                        self.camera.pos,
                        self.camera.pos + self.camera.front,
                        self.camera.up
                    ),
                    'projection': glm.perspective(
                        glm.radians(self.camera.zoom),
                        aspect_ratio,
                        0.1,
                        100.0
                    )
                }
            )
            last_frame = current_frame

            pygame.display.flip()
            self.clock.tick(60)

    @staticmethod
    def quit():
        """
        Quit the application.
        """
        pygame.quit()
        sys.exit()
