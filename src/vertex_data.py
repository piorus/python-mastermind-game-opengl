import utils
import glm
from math import pi, sin, cos
from OpenGL.GLU import *

SPHERE_STACK_COUNT = 36
SPHERE_SECTOR_COUNT = 18
SPHERE_RADIUS = 3


class VertexData:
    def __init__(self):
        self.is_loaded = False

    def load(self):
        pass

    def free(self):
        pass


# source: http://www.songho.ca/opengl/gl_sphere.html
class SphereVertexData(VertexData):
    VERTICES_TYPE = GLfloat
    INDICES_TYPE = GLint

    def __init__(self):
        super().__init__()

        self.vertices = []
        self.vertices_count = 0
        self.indices = []
        self.indices_count = 0

    def load(self):
        stack_step = pi / SPHERE_STACK_COUNT
        sector_step = 2 * pi / SPHERE_SECTOR_COUNT

        for i in range(SPHERE_STACK_COUNT + 1):
            stack_angle = pi / 2 - i * stack_step
            xy = SPHERE_RADIUS * cos(stack_angle)
            z = SPHERE_RADIUS * sin(stack_angle)

            k1 = i * (SPHERE_SECTOR_COUNT + 1)
            k2 = k1 + SPHERE_SECTOR_COUNT + 1

            for j in range(SPHERE_SECTOR_COUNT + 1):
                sector_angle = j * sector_step
                x = xy * cos(sector_angle)
                y = xy * sin(sector_angle)

                self.vertices += [*glm.normalize(glm.vec3(x, y, z))]

                if i != 0:
                    self.indices += [k1, k2, k1 + 1]

                if i != SPHERE_STACK_COUNT - 1:
                    self.indices += [k1 + 1, k2, k2 + 1]

                k1 += 1
                k2 += 1

        self.vertices_count = len(self.vertices)
        self.indices_count = len(self.indices)

        self.vertices = utils.type_cast(self.vertices, SphereVertexData.VERTICES_TYPE)
        self.indices = utils.type_cast(self.indices, SphereVertexData.INDICES_TYPE)

        self.is_loaded = True

        return self

    def free(self):
        self.__init__()


class VertexDataContainer:
    def __init__(self):
        self.children = {
            'sphere': SphereVertexData,
        }

    def load(self, key):
        data = self.children[key]().load() if key in self.children else None
        if not data:
            raise RuntimeError('Vertex data for %s is not available.' % key)

        return data


# data = {}
#
# data['plane'] = {
#     "vertices": {
#         "data": [
#             5.0, -0.5, 5.0, 2.0, 0.0,
#             -5.0, -0.5, 5.0, 0.0, 0.0,
#             -5.0, -0.5, -5.0, 0.0, 2.0,
#
#             5.0, -0.5, 5.0, 2.0, 0.0,
#             -5.0, -0.5, -5.0, 0.0, 2.0,
#             5.0, -0.5, -5.0, 2.0, 2.0
#         ],
#         "type": GLfloat
#     }
# }
#
# for k1 in data:
#     for k2 in data[k1]:
#         if isinstance(data[k1][k2], dict):
#             object = data[k1][k2]
#             data[k1][k2] = utils.type_cast(object["data"], object["type"])
#
#
# def get_vertices(name):
#     return data[name]["vertices"]
#
#
# def get_indices(name):
#     return data[name]["indices"]
#
#
# def get_indices_count(name):
#     return data[name]["indices_count"]
