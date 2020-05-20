"""
source: https://rusin.work/programming/modern-opengl-shader-helper-python/

This module contains Shader class, which is used to handle GLSL shaders.
"""
import OpenGL.GL as GL
import glm


class Shader:
    """
    Shader class is used to create both vertex and fragment shader.
    It connects both of them in shader program which is stored in property.
    Shader class is widely used across the application to handle both rendering
    and dynamically passing data straight to the shader.
    """
    def __init__(self, vertex_path: str, fragment_path: str):
        print("\n=== Shader Program ===")
        print("Step 1 - creating vertex shader...")
        self.vertex = self.create_shader(
            GL.GL_VERTEX_SHADER,
            self.read_from_file(vertex_path)
        )
        print("Step 2 - creating fragment shader...")
        self.fragment = self.create_shader(
            GL.GL_FRAGMENT_SHADER,
            self.read_from_file(fragment_path)
        )
        self.program = self.create_shader_program(self.vertex, self.fragment)

    @staticmethod
    def create_shader_program(vertex_shader, fragment_shader):
        """
        Create shader program and attach both
        vertex and fragment shaders and link them together.
        """
        print("Step 3 - creating shader program...")
        shader_program = GL.glCreateProgram()
        print("Step 4 - attaching vertex & fragment shaders...")
        GL.glAttachShader(shader_program, vertex_shader)
        GL.glAttachShader(shader_program, fragment_shader)
        GL.glBindFragDataLocation(shader_program, 0, "outColor")
        print("Step 5 - linking shader program...")
        GL.glLinkProgram(shader_program)
        # pylint: disable=line-too-long
        print("OK. Shader program was created successfully. (shader_program: %d)\n" % shader_program)

        return shader_program

    @staticmethod
    def create_shader(shader_type, source):
        """compile a shader"""
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            raise RuntimeError(GL.glGetShaderInfoLog(shader))

        return shader

    @staticmethod
    def read_from_file(path: str):
        """Load shader source from the file."""
        print("Loading shader source from %s..." % path)
        with open(path, 'r') as file:
            return file.read()

    def use(self):
        """Use current program"""
        GL.glUseProgram(self.program)

    # ------------------------------------------------------------------------
    def get_location(self, location: str):
        """
        Get memory location of the passed string in the shader program.
        This is used by multiple methods below
        to send additional data straight into the shader.
        """
        return GL.glGetUniformLocation(self.program, location)

    # ------------------------------------------------------------------------
    def set_bool(self, location: str, value: bool):
        """Set bool value in the location"""
        GL.glUniform1i(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_int(self, location: str, value: int):
        """Set int value in the location"""
        GL.glUniform1i(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_float(self, location: str, value: float):
        """Set float value in the location"""
        GL.glUniform1f(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec2(self, location: str, value: glm.vec2):
        """Set 2-dimensional vector value in the location"""
        GL.glUniform2fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec3(self, location: str, value: glm.vec3):
        """Set 3-dimensional vector value in the location"""
        GL.glUniform3fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec4(self, location: str, value: glm.vec4):
        """Set 4-dimensional vector value in the location"""
        GL.glUniform4fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_mat2(self, location: str, mat: glm.mat2):
        """Set 2x2 matrix value in the location"""
        GL.glUniformMatrix2fv(self.get_location(location), 1, GL.GL_FALSE, glm.value_ptr(mat))

    # ------------------------------------------------------------------------
    def set_mat3(self, location: str, mat: glm.mat3):
        """Set 3x3 matrix value in the location"""
        GL.glUniformMatrix3fv(self.get_location(location), 1, GL.GL_FALSE, glm.value_ptr(mat))

    # ------------------------------------------------------------------------
    def set_mat4(self, location: str, mat: glm.mat4):
        """Set 4x4 matrix value in the location"""
        GL.glUniformMatrix4fv(self.get_location(location), 1, GL.GL_FALSE, glm.value_ptr(mat))
