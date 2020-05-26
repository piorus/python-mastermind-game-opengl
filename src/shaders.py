"""
source: https://rusin.work/programming/modern-opengl-shader-helper-python/

This module contains Shader class, which is used to handle GLSL shaders.
"""
import os
import sys

import glm
from OpenGL import GL


def create_shader_program(vertex_shader, fragment_shader):
    """
    Create shader program from vertex and fragment shaders.

    This function attach both vertex and fragment shaders
    to the program and link them together.

    :param vertex_shader: vertex shader ID
    :param fragment_shader: fragment shader ID
    :return: shader program ID
    """
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vertex_shader)
    GL.glAttachShader(program, fragment_shader)
    GL.glBindFragDataLocation(program, 0, "outColor")
    GL.glLinkProgram(program)

    return program


def create_shader(shader_type, source):
    """
    Compile a shader.

    :param shader_type: type of a shader to compile
    :param source: shader source code
    :return: shader ID
    """
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
        raise RuntimeError(GL.glGetShaderInfoLog(shader))

    return shader


def read_from_file(path: str):
    """
    Load shader source from the file.

    :param path: path to the shader source file
    :return: source file content
    """
    with open(os.path.join(os.path.dirname(sys.argv[0]), path), 'r') as file:
        return file.read()


class Shader:
    """
    Shader class is handy helper to manage GLSL shaders more efficiently.

    It compiles vertex and fragment shaders from the file, and links them together
    in a shader program.
    Shader class is widely used across the application to handle both rendering
    and dynamically passing data straight to the shader through uniform variables.
    """

    def __init__(self, vertex_path: str, fragment_path: str):
        self.program = create_shader_program(
            create_shader(
                GL.GL_FRAGMENT_SHADER,
                read_from_file(fragment_path)
            ),
            create_shader(
                GL.GL_VERTEX_SHADER,
                read_from_file(vertex_path)
            )
        )

    def use(self):
        """Use current program"""
        GL.glUseProgram(self.program)

    def get_location(self, name: str):
        """
        Get memory location of the uniform variable in the shader program.

        This is used by multiple methods below
        to send additional data straight into the shader.

        :param name: uniform variable name
        :return: location of the uniform variable
        """
        return GL.glGetUniformLocation(self.program, name)

    def set_bool(self, name: str, value: bool):
        """
        Set bool uniform variable.

        :param name: uniform variable name
        :param value: bool value to set
        :return None
        """
        GL.glUniform1i(self.get_location(name), glm.value_ptr(value))

    def set_int(self, name: str, value: int):
        """
        Set int uniform variable.

        :param name: uniform variable name
        :param value: int value to set
        :return None
        """
        GL.glUniform1i(self.get_location(name), glm.value_ptr(value))

    def set_float(self, name: str, value: float):
        """
        Set float uniform variable.

        :param name: uniform variable name
        :param value: float value to set
        :return None
        """
        GL.glUniform1f(self.get_location(name), GL.GLfloat(value))

    def set_vec2(self, name: str, value: glm.vec2):
        """
        Set 2-dimensional vector uniform variable.

        :param name: uniform variable name
        :param value: glm.vec2 value to set
        :return None
        """
        GL.glUniform2fv(self.get_location(name), 1, glm.value_ptr(value))

    def set_vec3(self, name: str, value: glm.vec3):
        """
        Set 3-dimensional vector uniform variable.

        :param name: uniform variable name
        :param value: glm.vec3 value to set
        :return None
        """
        GL.glUniform3fv(self.get_location(name), 1, glm.value_ptr(value))

    def set_vec4(self, name: str, value: glm.vec4):
        """
        Set 4-dimensional vector uniform variable.

        :param name: uniform variable name
        :param value: glm.vec4 value to set
        :return None
        """
        GL.glUniform4fv(self.get_location(name), 1, glm.value_ptr(value))

    def set_mat2(self, name: str, value: glm.mat2):
        """
        Set 2x2 matrix uniform variable.

        :param name: uniform variable name
        :param value: glm.mat2 value to set
        :return None
        """
        GL.glUniformMatrix2fv(self.get_location(name), 1, GL.GL_FALSE, glm.value_ptr(value))

    def set_mat3(self, name: str, value: glm.mat3):
        """
        Set 3x3 matrix uniform variable.

        :param name: uniform variable name
        :param value: glm.mat3 value to set
        :return None
        """
        GL.glUniformMatrix3fv(self.get_location(name), 1, GL.GL_FALSE, glm.value_ptr(value))

    def set_mat4(self, name: str, value: glm.mat4):
        """
        Set 4x4 matrix uniform variable.

        :param name: uniform variable name
        :param value: glm.mat4 value to set
        :return None
        """
        GL.glUniformMatrix4fv(self.get_location(name), 1, GL.GL_FALSE, glm.value_ptr(value))
