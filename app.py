import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from bootstrap import events, run

def draw(event):
    pass

events.on(events.DRAW, draw)

glEnable(GL_DEPTH_TEST)
run()
