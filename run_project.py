import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import OpenGL.GL as GL
import pygame

from app import App


def main():
    """
    Wrapper function executed directly after starting the program.

    It is used to create App class, and to run the application.
    It also set OpenGL constants used in the game.
    """
    pygame.init()

    app = App()

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)  # blend is used in GUI texts
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    app.register_events()
    app.run()


if __name__ == '__main__':
    main()
