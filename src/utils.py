import pygame, os
from OpenGL.GL import *
from ctypes import sizeof, c_void_p


def type_cast(what, type):
    return (type * len(what))(*what)


def surface_to_texture(
        surface,
        texture: int = None,
        flipped: bool = False,
        wrap_s=GL_REPEAT,
        wrap_t=GL_REPEAT,
        min_filter=GL_LINEAR,
        mag_filter=GL_LINEAR
):
    surface_width, surface_height = surface.get_size()
    surface_data = pygame.image.tostring(surface, 'RGBA', flipped)

    texture = texture if texture else glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # textures - wrapping
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
    # textures - filtering
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, mag_filter)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        surface_width,
        surface_height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        surface_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture


def load_texture(image_path, wrap_s=GL_REPEAT, wrap_t=GL_REPEAT, min_filter=GL_LINEAR, mag_filter=GL_LINEAR):
    return surface_to_texture(
        pygame.image.load(image_path),
        flipped=os.path.splitext(image_path)[1] != '.png',
        wrap_s=wrap_s,
        wrap_t=wrap_t,
        min_filter=min_filter,
        mag_filter=mag_filter
    )


class OpenGLObject:
    def __init__(self, vao, vbo):
        self.vao = vao
        self.vbo = vbo


class OpenGLObjectFactory:
    def __init__(self):
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.stride = None
        self.vertices = None
        self.indices = None
        self.attrib_pointers = []

    def set_vertices(self, vertices):
        self.vertices = vertices
        return self

    def set_indices(self, indices):
        self.indices = indices
        return self

    def set_stride(self, stride):
        self.stride = stride
        return self

    def set_vbo(self, vbo):
        self.vbo = vbo
        return self

    def set_vao(self, vao):
        self.vao = vao
        return self

    def set_attrib_pointer(self, index, size, type, normalized, offset):
        if not self.stride:
            raise RuntimeError('Please set_stride(stride) before set_attrib_pointer().')
        self.attrib_pointers.append({
            'index': index,
            'size': size,
            'type': type,
            'normalized': normalized,
            'stride': self.stride,
            'offset': c_void_p(offset * sizeof(GLfloat))
        })
        return self

    def create(self):
        self.vbo = self.vbo if self.vbo else glGenBuffers(1)
        self.vao = self.vao if self.vao else glGenVertexArrays(1)
        if not self.stride:
            raise RuntimeError('Please set_stride(stride) before create().')

        glBindVertexArray(self.vao)

        if self.vertices:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)

        if self.indices:
            self.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(self.indices), self.indices, GL_STATIC_DRAW)

        for attrib_pointer in self.attrib_pointers:
            glEnableVertexAttribArray(attrib_pointer['index'])
            glVertexAttribPointer(*attrib_pointer.values())

        glBindVertexArray(0)

        vao, vbo = self.vao, self.vbo
        self.__init__()  # reset

        return OpenGLObject(vao=vao, vbo=vbo)
