"""Sphere class"""
from ctypes import sizeof

import OpenGL.GL as GL
import glm

import shaders
from vertex_data import SphereVertexData
from game.objects3d.opengl_object import OpenGLObject


# pylint: disable=too-many-arguments,too-few-public-methods
class Sphere(OpenGLObject):
    """
    Sphere class is used to render all of the spheres in the game by using
    the same set of vertices and indices with different models (positions) in the space.
    """

    def __init__(self):
        super().__init__()

        data = SphereVertexData().load()

        self.vertices = data.vertices
        self.indices = data.indices
        self.indices_count = data.indices_count
        self.stride = 3 * sizeof(GL.GLfloat)
        self.shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')
        self.set_attrib_pointer(
            index=0,
            size=3,
            attrib_type=GL.GL_FLOAT,
            normalized=GL.GL_FALSE,
            offset=0
        )

        self.buffer_data_to_gpu()

    def draw(
            self,
            model: glm.mat4,
            view: glm.mat4,
            projection: glm.mat4,
            color: glm.vec3,
            scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
            show_wireframe: bool = False
    ):
        """
        Draw a sphere using model, view and projection matrices.

        :param model: 4x4 model matrix
        :param view: 4x4 view matrix
        :param projection: 4x4 projection matrix
        :param color: glm.vec3 representing color of the sphere
        :param scale: glm.vec3 representing scale of the sphere
        :param show_wireframe: flag that determine if wireframe should be displayed
        :return:
        """
        self.shader.use()
        self.shader.set_mat4('model', glm.scale(model, scale))
        self.shader.set_mat4('view', view)
        self.shader.set_mat4('projection', projection)
        self.shader.set_vec3('aColor', color)

        if show_wireframe:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        GL.glBindVertexArray(self.vao)

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self.indices_count,
            GL.GL_UNSIGNED_INT,
            None
        )

        if show_wireframe:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
