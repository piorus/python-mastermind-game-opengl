import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from bootstrap import events, run
from utils import load_texture, ObjectFactory
import shaders
import vertex_data

factory = ObjectFactory()

factory \
    .set_vertices(vertex_data.get_vertices('cube')) \
    .set_stride(5 * sizeof(GLfloat)) \
    .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0) \
    .set_attrib_pointer(index=1, size=2, type=GL_FLOAT, normalized=GL_FALSE, offset=3)

cube = factory.create()
cube_texture = load_texture('assets/pepe.jpg')
active_cube_texture = load_texture('assets/cat.png')

cube_coordinates = [
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
active_cubes = [1] + [0] * (len(cube_coordinates) - 1)

shader = shaders.Shader('shaders/shader.vert', 'shaders/shader.frag')

def draw(event):
    shader.use()
    shader.set_mat4('view', event.view)
    shader.set_mat4('projection', event.projection)

    glBindVertexArray(cube.vao)

    for k, coords in enumerate(cube_coordinates):
        glBindTexture(GL_TEXTURE_2D, active_cube_texture if active_cubes[k] else cube_texture)
        model = glm.translate(glm.mat4(1.0), coords)
        shader.set_mat4('model', model)
        glDrawArrays(GL_TRIANGLES, 0, 36)

events.on(events.DRAW, draw)

def activate_cube(event):
    index = active_cubes.index(1)
    active_cubes[index] = 0
    next_index = index + 1 if index != len(active_cubes) - 1 else 0
    active_cubes[next_index] = 1

events.on(pygame.KEYDOWN, activate_cube, conditions={'key': pygame.K_SPACE})

glEnable(GL_DEPTH_TEST)
run()
