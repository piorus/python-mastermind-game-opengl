# source: https://rusin.work/programming/modern-opengl-text-rendering-in-pygame/

import pygame
from OpenGL.GL import *
from ctypes import sizeof, c_void_p

from shaders import Shader
from utils import surface_to_texture

DEFAULT_VERTEX_SHADER = '''
    #version 330 core
    layout (location = 0) in vec2 aPos;
    layout (location = 1) in vec2 aTexCoords;

    out vec2 TexCoords;

    void main()
    {
        TexCoords = aTexCoords;
        gl_Position = vec4(aPos, 0.0, 1.0);
    }
'''

DEFAULT_FRAGMENT_SHADER = '''
    #version 330 core
    out vec4 FragColor;

    in vec2 TexCoords;

    uniform sampler2D texture1;

    void main()
    {
      FragColor = texture(texture1, TexCoords);
    }
'''


def get_default_shader():
    vertex = Shader.create_shader(GL_VERTEX_SHADER, DEFAULT_VERTEX_SHADER)
    fragment = Shader.create_shader(GL_FRAGMENT_SHADER, DEFAULT_FRAGMENT_SHADER)
    shader_program = Shader.create_shader_program(vertex, fragment)
    glUseProgram(shader_program)
    glUniform1i(glGetUniformLocation(shader_program, 'texture1'), 0)

    return shader_program


def pygameize_color(color):
    return None if color is None or color[3] == 0.0 else [i * 255 for i in color]


class Text:
    def __init__(
            self,
            text,
            shader,
            position=(0.0, 0.0),
            font_name='dejavusans',
            font_size=60,
            font_color=(1.0, 1.0, 0.0, 1.0),
            bg_color=None
    ):
        x, y = position
        self.x = x
        self.y = y
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color

        self.shader = shader
        self.texture = glGenTextures(1)
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        self.ebo = glGenBuffers(1)

        self.is_prepared = False
        self.prepare()

    def prepare(self):
        font = pygame.font.SysFont(self.font_name, self.font_size)
        surface = font.render(self.text, True, pygameize_color(self.font_color), pygameize_color(self.bg_color))
        # copy surface data to openGL texture
        surface_to_texture(surface, self.texture, True)
        # calc vertex positions
        xres, yres = pygame.display.get_surface().get_size()
        width, height = surface.get_size()
        x1 = width / xres / 2
        y1 = height / yres / 2

        vertices = [
            self.x + x1, self.y + y1, 1.0, 1.0,  # top right
            self.x + x1, self.y - y1, 1.0, 0.0,  # bottom right
            self.x - x1, self.y - y1, 0.0, 0.0,  # bottom left
            self.x - x1, self.y + y1, 0.0, 1.0,  # top left
        ]
        vertices = (GLfloat * len(vertices))(*vertices)  # cast to GLfloat

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_DYNAMIC_DRAW)

        elements = [
            0, 1, 3,
            1, 2, 3
        ]
        elements = (GLuint * len(elements))(*elements)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(elements), elements, GL_DYNAMIC_DRAW)

        glBindVertexArray(self.vao)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
        glBindVertexArray(0)

        self.is_prepared = True

    def draw(self):
        if not self.is_prepared:
            return

        glUseProgram(self.shader)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def set_text(self, text):
        self.text = text
        self.is_prepared = False
        self.prepare()
        return self
