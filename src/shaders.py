# source: https://rusin.work/programming/modern-opengl-shader-helper-python/
from OpenGL.GL import *
import glm


class Shader:
    def __init__(self, vertex_path: str, fragment_path: str):
        print("\n=== Shader Program ===")
        print("Step 1 - creating vertex shader...")
        self.vertex = self.create_shader(GL_VERTEX_SHADER, self.read_from_file(vertex_path))
        print("Step 2 - creating fragment shader...")
        self.fragment = self.create_shader(GL_FRAGMENT_SHADER, self.read_from_file(fragment_path))
        self.program = self.create_shader_program(self.vertex, self.fragment)

    @staticmethod
    def create_shader_program(vertex_shader, fragment_shader):
        print("Step 3 - creating shader program...")
        shader_program = glCreateProgram()
        print("Step 4 - attaching vertex & fragment shaders...")
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glBindFragDataLocation(shader_program, 0, "outColor")
        print("Step 5 - linking shader program...")
        glLinkProgram(shader_program)
        print("OK. Shader program was created successfully. (shader_program: %d)\n" % shader_program)

        return shader_program

    @staticmethod
    def create_shader(shader_type, source):
        """compile a shader"""
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader))

        return shader

    @staticmethod
    def read_from_file(path: str):
        print("Loading shader source from %s..." % path)
        with open(path, 'r') as file:
            return file.read()

    def use(self):
        glUseProgram(self.program)

    # ------------------------------------------------------------------------
    def get_location(self, location: str):
        return glGetUniformLocation(self.program, location)

    # ------------------------------------------------------------------------
    def set_bool(self, location: str, value: bool):
        glUniform1i(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_int(self, location: str, value: int):
        glUniform1i(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_float(self, location: str, value: float):
        glUniform1f(self.get_location(location), glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec2(self, location: str, value: glm.vec2):
        glUniform2fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec3(self, location: str, value: glm.vec3):
        glUniform3fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_vec4(self, location: str, value: glm.vec4):
        glUniform4fv(self.get_location(location), 1, glm.value_ptr(value))

    # ------------------------------------------------------------------------
    def set_mat2(self, location: str, mat: glm.mat2):
        glUniformMatrix2fv(self.get_location(location), 1, GL_FALSE, glm.value_ptr(mat))

    # ------------------------------------------------------------------------
    def set_mat3(self, location: str, mat: glm.mat3):
        glUniformMatrix3fv(self.get_location(location), 1, GL_FALSE, glm.value_ptr(mat))

    # ------------------------------------------------------------------------
    def set_mat4(self, location: str, mat: glm.mat4):
        glUniformMatrix4fv(self.get_location(location), 1, GL_FALSE, glm.value_ptr(mat))
