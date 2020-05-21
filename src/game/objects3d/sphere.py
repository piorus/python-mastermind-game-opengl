"""Sphere class"""

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

        self.shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')
        data = SphereVertexData().load()

        self.set_vertices(data.vertices)
        self.set_indices(data.indices)
        self.set_stride(3 * GL.sizeof(GL.GLfloat))
        self.set_attrib_pointer(
            index=0,
            size=3,
            _type=GL.OpenGL.GL.GL_FLOAT,
            normalized=GL.GL_FALSE,
            offset=0
        )
        self.indices_count = data.indices_count

        self.buffer_data_to_gpu()

    def draw(
            self,
            model: glm.vec3,
            view: glm.vec3,
            projection: glm.vec3,
            color: glm.vec3,
            scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
            show_wireframe: bool = False
    ):
        """draw a sphere using view projection model"""

        GL.glBindVertexArray(self.vao)

        self.shader.use()
        self.shader.set_mat4('model', glm.scale(model, scale))
        self.shader.set_mat4('view', view)
        self.shader.set_mat4('projection', projection)
        self.shader.set_vec3('aColor', color)

        if show_wireframe:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self.indices_count,
            GL.GL_UNSIGNED_INT,
            None
        )

        if show_wireframe:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
