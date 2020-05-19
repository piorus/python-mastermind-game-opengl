from ctypes import sizeof

import glm
from OpenGL.GL import *

import shaders
import vertex_data
from utils import ObjectFactory


class Sphere:
    def __init__(self):
        self.shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')

        factory = ObjectFactory()
        vertex_data_container = vertex_data.VertexDataContainer()
        data = vertex_data_container.load('sphere')

        factory \
            .set_vertices(data.vertices) \
            .set_indices(data.indices) \
            .set_stride(3 * sizeof(GLfloat)) \
            .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0)

        self.object = factory.create()
        self.indices_count = data.indices_count

        data.free()

    def draw(
            self,
            model: glm.vec3,
            view: glm.vec3,
            projection: glm.vec3,
            color: glm.vec3,
            scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
            show_wireframe: bool = False
    ):
        glBindVertexArray(self.object.vao)

        self.shader.use()
        self.shader.set_mat4('model', glm.scale(model, scale))
        self.shader.set_mat4('view', view)
        self.shader.set_mat4('projection', projection)
        self.shader.set_vec3('aColor', color)

        if show_wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glDrawElements(GL_TRIANGLES, self.indices_count, GL_UNSIGNED_INT, None)

        if show_wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)