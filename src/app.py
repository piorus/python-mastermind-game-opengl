import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from bootstrap import events, run
from utils import load_texture, ObjectFactory
import shaders
import vertex_data
#@TODO replace it with static colors later on
import random

factory = ObjectFactory()

factory \
    .set_vertices(vertex_data.get_vertices('sphere')) \
    .set_indices(vertex_data.get_indices('sphere')) \
    .set_stride(3 * sizeof(GLfloat)) \
    .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0)
sphere = factory.create()

factory \
    .set_vertices(vertex_data.get_vertices('plane')) \
    .set_stride(5 * sizeof(GLfloat)) \
    .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0) \
    .set_attrib_pointer(index=1, size=2, type=GL_FLOAT, normalized=GL_FALSE, offset=3)
plane = factory.create()

sphere_shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')

def draw_sphere(event):
    sphere_shader.use()

    sphere_shader.set_mat4('view', event.view)
    sphere_shader.set_mat4('projection', event.projection)

    glBindVertexArray(sphere.vao)

    for row in range(24):
        for col in range(2):
            model = glm.translate(glm.mat4(1.0), glm.vec3(col, 0.0, -1.25 + row))
            sphere_shader.set_mat4('model', glm.scale(model, glm.vec3(0.25, 0.25, 0.25)))
            sphere_shader.set_vec3('aColor', glm.vec3(1.0, 0.0, 0.0) if col % 2 else glm.vec3(1.0, 1.0, 1.0))
            glDrawElements(GL_TRIANGLES, vertex_data.get_indices_count('sphere'), GL_UNSIGNED_INT, None)

    for row in range(12):
        for col in range(4):
            model = glm.translate(glm.mat4(1.0), glm.vec3(-10 - col * (-2.5), 0.0, row * 2.5))
            sphere_shader.set_mat4('model', glm.scale(model, glm.vec3(1.0, 1.0, 1.0)))
            sphere_shader.set_vec3('aColor', glm.vec3(0.0, 1.0, 0.0))
            glDrawElements(GL_TRIANGLES, vertex_data.get_indices_count('sphere'), GL_UNSIGNED_INT, None)

events.on(events.DRAW, draw_sphere)

# events.on(pygame.KEYDOWN, activate_cube, conditions={'key': pygame.K_SPACE})

glEnable(GL_DEPTH_TEST)
run()
