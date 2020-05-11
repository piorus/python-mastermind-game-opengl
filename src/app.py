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

coordinates = [
    glm.vec3( 0.0,  0.0,  0.0),
    glm.vec3( 2.0,  5.0, -15.0),
    glm.vec3(-1.5, -2.2, -2.5),
    glm.vec3(-3.8, -2.0, -12.3),
    glm.vec3( 2.4, -0.4, -3.5),
    glm.vec3(-1.7,  3.0, -7.5),
    glm.vec3( 1.3, -2.0, -2.5),
    glm.vec3( 1.5,  2.0, -2.5),
    glm.vec3( 1.5,  0.2, -1.5),
    glm.vec3(-1.3,  1.0, -1.5)
]

sphere_shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')

def draw_sphere(event):
    sphere_shader.use()

    sphere_shader.set_mat4('view', event.view)
    sphere_shader.set_mat4('projection', event.projection)

    glBindVertexArray(sphere.vao)

    for k, coords in enumerate(coordinates):
        model = glm.translate(glm.mat4(1.0), coords)
        sphere_shader.set_mat4('model', model)
        sphere_shader.set_vec3('aColor', glm.vec3(random.randint(0, 10) / 10, random.randint(0, 10) / 10, random.randint(0, 10) / 10))
        glDrawElements(GL_TRIANGLES, vertex_data.get_indices_count('sphere'), GL_UNSIGNED_INT, None)

events.on(events.DRAW, draw_sphere)

# events.on(pygame.KEYDOWN, activate_cube, conditions={'key': pygame.K_SPACE})

glEnable(GL_DEPTH_TEST)
run()
