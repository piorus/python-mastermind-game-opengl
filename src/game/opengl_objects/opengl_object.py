"""base class for OpenGL objects"""
from ctypes import sizeof, c_void_p

import OpenGL.GL as GL


# pylint: disable=too-many-arguments
class OpenGLObject:
    """
    OpenGLObject is setting up initial object properiies
    and buffer vertices/indices data straight to the GPU.
    """

    def __init__(
            self,
            vao=None,
            vbo=None,
            ebo=None,
            stride=None,
            vertices=None,
            indices=None,
            attrib_pointers=None
    ):
        if attrib_pointers is None:
            attrib_pointers = []
        self.vao = vao
        self.vbo = vbo
        self.ebo = ebo
        self.stride = stride
        self.vertices = vertices
        self.indices = indices
        self.attrib_pointers = attrib_pointers

    def set_attrib_pointer(self, index, size, attrib_type, normalized, offset):
        """attrib_pointer setter"""
        if not self.stride:
            raise RuntimeError('Please set_stride(stride) before set_attrib_pointer().')
        self.attrib_pointers.append({
            'index': index,
            'size': size,
            'type': attrib_type,
            'normalized': normalized,
            'stride': self.stride,
            'offset': c_void_p(offset * sizeof(GL.GLfloat))
        })
        return self

    def buffer_data_to_gpu(self):
        """
        This method is used to buffer vertices/indices data
        straight to the GPU for better performance during rendering.
        Data needs to be buffered only once, as long as vertices do not change.
        """
        self.vbo = self.vbo if self.vbo else GL.glGenBuffers(1)
        self.vao = self.vao if self.vao else GL.glGenVertexArrays(1)
        if not self.stride:
            raise RuntimeError('Please set_stride(stride) before create().')

        GL.glBindVertexArray(self.vao)

        if self.vertices:
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
            GL.glBufferData(
                target=GL.GL_ARRAY_BUFFER,
                size=GL.sizeof(self.vertices),
                data=self.vertices,
                usage=GL.GL_STATIC_DRAW
            )

        if self.indices:
            self.ebo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            GL.glBufferData(
                target=GL.GL_ELEMENT_ARRAY_BUFFER,
                size=GL.sizeof(self.indices),
                data=self.indices,
                usage=GL.GL_STATIC_DRAW
            )

        for attrib_pointer in self.attrib_pointers:
            GL.glEnableVertexAttribArray(attrib_pointer['index'])
            GL.glVertexAttribPointer(*attrib_pointer.values())

        GL.glBindVertexArray(0)
