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

shader = shaders.Shader('shaders/shader.vert', 'shaders/shader.frag')

def draw(event):
    glBindTexture(GL_TEXTURE_2D, cube_texture)

    shader.use()
    shader.set_mat4('view', event.view)
    shader.set_mat4('projection', event.projection)

    glBindVertexArray(cube.vao)

    model = glm.translate(glm.mat4(1.0), glm.vec3(-1.0, 0.0, -1.0))
    shader.set_mat4('model', model)
    glDrawArrays(GL_TRIANGLES, 0, 36)

    model = glm.translate(glm.mat4(1.0), glm.vec3(2.0, 0.0, 0.0))
    shader.set_mat4('model', model)
    glDrawArrays(GL_TRIANGLES, 0, 36)

events.on(events.DRAW, draw)

glEnable(GL_DEPTH_TEST)
run()
