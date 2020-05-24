"""
Vertices and indices data of the game 3D objects.

source: http://www.songho.ca/opengl/gl_sphere.html
"""

from math import pi, sin, cos

import glm
import OpenGL.GLU as GLU

import utils

SPHERE_STACK_COUNT = 36
SPHERE_SECTOR_COUNT = 18
SPHERE_RADIUS = 3
SPHERE_LENGTH_INV = 1.0


# pylint: disable=too-few-public-methods
class SphereVertexData:
    """
    Sphere vertices and indices casted to GLfloat and Glint.
    """
    VERTICES_TYPE = GLU.GLfloat
    INDICES_TYPE = GLU.GLint

    def __init__(self):
        super().__init__()

        self.vertices = []
        self.vertices_count = 0
        self.indices = []
        self.indices_count = 0

    # pylint: disable=too-many-locals
    def load(self):
        """
        Generate sphere vertices and indices
        using predefined stack count, sector count and radius.
        Then, cast it to type supported by OpenGL.
        """
        stack_step = pi / SPHERE_STACK_COUNT
        sector_step = 2 * pi / SPHERE_SECTOR_COUNT

        for i in range(SPHERE_STACK_COUNT + 1):
            stack_angle = pi / 2 - i * stack_step
            _xy = SPHERE_RADIUS * cos(stack_angle)
            _z = SPHERE_RADIUS * sin(stack_angle)

            k_1 = i * (SPHERE_SECTOR_COUNT + 1)
            k_2 = k_1 + SPHERE_SECTOR_COUNT + 1

            for j in range(SPHERE_SECTOR_COUNT + 1):
                sector_angle = j * sector_step
                _x = _xy * cos(sector_angle)
                _y = _xy * sin(sector_angle)

                _nx = _x * SPHERE_LENGTH_INV
                _ny = _y * SPHERE_LENGTH_INV
                _nz = _z * SPHERE_LENGTH_INV

                self.vertices += [
                    *glm.normalize(glm.vec3(_x, _y, _z)), # position
                    *glm.normalize(glm.vec3(_nx, _ny, _nz)) # normals
                ]

                if i != 0:
                    self.indices += [k_1, k_2, k_1 + 1]

                if i != SPHERE_STACK_COUNT - 1:
                    self.indices += [k_1 + 1, k_2, k_2 + 1]

                k_1 += 1
                k_2 += 1

        self.vertices_count = len(self.vertices)
        self.indices_count = len(self.indices)

        self.vertices = utils.type_cast(self.vertices, SphereVertexData.VERTICES_TYPE)
        self.indices = utils.type_cast(self.indices, SphereVertexData.INDICES_TYPE)

        return self
