"""
source: https://rusin.work/programming/modern-opengl-text-rendering-in-pygame/

text module is handling OpenGL text rendering by copying pygame surface into the OpenGL texture.
"""

from ctypes import sizeof, c_void_p

import pygame
import OpenGL.GL as GL

from shaders import Shader
from utils import surface_to_texture, type_cast

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
    """
    Returns default shader program used to render text by compiling
    DEFAULT_VERTEX_SHADER and DEFAULT_FRAGMENT_SHADER then joining them together.
    """
    vertex = Shader.create_shader(GL.GL_VERTEX_SHADER, DEFAULT_VERTEX_SHADER)
    fragment = Shader.create_shader(GL.GL_FRAGMENT_SHADER, DEFAULT_FRAGMENT_SHADER)
    shader_program = Shader.create_shader_program(vertex, fragment)
    GL.glUseProgram(shader_program)
    GL.glUniform1i(GL.glGetUniformLocation(shader_program, 'texture1'), 0)

    return shader_program


def pygameize_color(color):
    """
    Convert normalized color (0-1) to RGB (0-255).

    :param color: normalized color (0-1, 0-1, 0-1)
    :return: RGB color (0-255, 0-255, 0-255)
    """
    return None if color is None or color[3] == 0.0 else [i * 255 for i in color]

# pylint: disable=too-many-instance-attributes,too-many-arguments
class Text:
    """
    Text class is handling text rendering by copying
    pygame surface data into the OpenGL texture.
    Rendering can be handled by any shader program
    passed as a constructor argument.
    """
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
        _x, _y = position
        self._x = _x
        self._y = _y
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color

        self.shader = shader
        self.texture = GL.glGenTextures(1)
        self.vbo = GL.glGenBuffers(1)
        self.vao = GL.glGenVertexArrays(1)
        self.ebo = GL.glGenBuffers(1)

        self.is_prepared = False
        self.prepare()

    def prepare(self):
        """
        Prepare text to render in OpenGL context by:
          1. creating pygame font
          2. rendering text passed to the constructor using font
          3. converting pygame surface to OpenGL texture by copying surface data
             to the texture
          4. calculating text position
        """
        font = pygame.font.SysFont(self.font_name, self.font_size)
        surface = font.render(
            self.text,
            True,
            pygameize_color(self.font_color),
            pygameize_color(self.bg_color)
        )
        # copy surface data to openGL texture
        surface_to_texture(surface, self.texture, True)
        # calc vertex positions
        res_x, res_y = pygame.display.get_surface().get_size()
        width, height = surface.get_size()
        offset_x = width / res_x / 2
        offset_y = height / res_y / 2

        vertices = [
            self._x + offset_x, self._y + offset_y, 1.0, 1.0,  # top right
            self._x + offset_x, self._y - offset_y, 1.0, 0.0,  # bottom right
            self._x - offset_x, self._y - offset_y, 0.0, 0.0,  # bottom left
            self._x - offset_x, self._y + offset_y, 0.0, 1.0,  # top left
        ]
        vertices = type_cast(vertices, GL.GLfloat)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, GL.sizeof(vertices), vertices, GL.GL_DYNAMIC_DRAW)

        elements = [
            0, 1, 3,
            1, 2, 3
        ]
        elements = type_cast(elements, GL.GLuint)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(
            target=GL.GL_ELEMENT_ARRAY_BUFFER,
            size=sizeof(elements),
            data=elements,
            usage=GL.GL_DYNAMIC_DRAW
        )

        GL.glBindVertexArray(self.vao)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(
            index=0,
            size=2,
            type=GL.GL_FLOAT,
            normalized=GL.GL_FALSE,
            stride=4 * GL.sizeof(GL.GLfloat),
            pointer=c_void_p(0)
        )
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(
            index=1,
            size=2,
            type=GL.GL_FLOAT,
            normalized=GL.GL_FALSE,
            stride=4 * GL.sizeof(GL.GLfloat),
            pointer=c_void_p(2 * sizeof(GL.GLfloat))
        )
        GL.glBindVertexArray(0)

        self.is_prepared = True

    def draw(self):
        """
        Draw text on the screen.
        """
        if not self.is_prepared:
            return

        GL.glUseProgram(self.shader)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def set_text(self, text: str):
        """
        Set text and copy surface data to the OpenGL texture.

        :param text: new text value
        :return:
        """
        self.text = text
        self.is_prepared = False
        self.prepare()

        return self
