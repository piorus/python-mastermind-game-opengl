"""
source: https://rusin.work/programming/modern-opengl-text-rendering-in-pygame/

text module is handling OpenGL text rendering by copying pygame surface into the OpenGL texture.
"""

from ctypes import sizeof, c_void_p

import glm
from OpenGL import GL
import pygame

from src import shaders
from src import utils

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

DEFAULT_POSITION = glm.vec2(0.0, 0.0)
DEFAULT_FONT_NAME = 'dejavusans'
DEFAULT_FONT_SIZE = 60
DEFAULT_FONT_COLOR = glm.vec4(1.0, 1.0, 0.0, 1.0)


def get_default_shader():
    """
    Returns default shader program used to render text.

    DEFAULT_VERTEX_SHADER and DEFAULT_FRAGMENT_SHADER are compiled
    and then joined together in a shader program which is returned.

    :return shader program ID
    """
    vertex = shaders.create_shader(GL.GL_VERTEX_SHADER, DEFAULT_VERTEX_SHADER)
    fragment = shaders.create_shader(GL.GL_FRAGMENT_SHADER, DEFAULT_FRAGMENT_SHADER)
    shader_program = shaders.create_shader_program(vertex, fragment)
    GL.glUseProgram(shader_program)
    GL.glUniform1i(GL.glGetUniformLocation(shader_program, 'texture1'), 0)

    return shader_program


def pygameize_color(color):
    """
    Convert normalized color (0-1) to RGBA (0-255).

    Return None in case if no color is passed or transparency is set to 0

    :param color: normalized color (0-1, 0-1, 0-1, 0-1)
    :return: RGB color (0-255, 0-255, 0-255, 0-255)
    """
    return None if color is None or color[3] == 0.0 else [i * 255 for i in color]


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Text:
    """
    Text class is handling text rendering.

    Internally, it is using pygame.font to render text,
    and copy surface data into the OpenGL texture.
    Rendering can be handled by any shader program
    passed as a constructor argument.
    """

    def __init__(
            self,
            text,
            shader,
            position=DEFAULT_POSITION,
            font_name=DEFAULT_FONT_NAME,
            font_size=DEFAULT_FONT_SIZE,
            font_color=DEFAULT_FONT_COLOR,
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

    def load(self, text):
        """
        Prepare text to render in OpenGL context.

        List of steps in execution order:
          1. create pygame font
          2. render text passed to the constructor using pygame font
          3. convert pygame surface to OpenGL texture by copying surface data
             to the texture
          4. calculate text position
          5. send updated vertices / indices data to the GPU
        """
        font = pygame.font.SysFont(self.font_name, self.font_size)
        surface = font.render(
            text,
            True,
            pygameize_color(self.font_color),
            pygameize_color(self.bg_color)
        )
        # copy surface data to openGL texture
        self.texture = utils.surface_to_texture(surface, flipped=True)

        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)

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
        vertices = utils.type_cast(vertices, GL.GLfloat)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, GL.sizeof(vertices), vertices, GL.GL_STATIC_DRAW)

        indices = [
            0, 1, 3,
            1, 2, 3
        ]
        indices = utils.type_cast(indices, GL.GLuint)
        GL.glBufferData(
            target=GL.GL_ELEMENT_ARRAY_BUFFER,
            size=sizeof(indices),
            data=indices,
            usage=GL.GL_DYNAMIC_DRAW
        )
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
            self.load(self.text)

        GL.glUseProgram(self.shader)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)

    def set_text(self, text: str):
        """
        Set text and copy surface data to the OpenGL texture.

        :param text: new text value
        """
        self.text = text
        self.is_prepared = False
