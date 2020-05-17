import utils
import glm
from math import pi, sin, cos
from OpenGL.GL import *
from OpenGL.GLU import *

data = {}

data["cube"] = {
    "vertices": {
        "data": [
            #   positions    texture Coords
            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0,

            -0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,

            -0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 0.0,

            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,

            -0.5, -0.5, -0.5, 0.0, 1.0,
            0.5, -0.5, -0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 1.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 0.0, 1.0
        ],
        "type": GLfloat
    }
}

data['plane'] = {
    "vertices": {
        "data": [
            5.0, -0.5, 5.0, 2.0, 0.0,
            -5.0, -0.5, 5.0, 0.0, 0.0,
            -5.0, -0.5, -5.0, 0.0, 2.0,

            5.0, -0.5, 5.0, 2.0, 0.0,
            -5.0, -0.5, -5.0, 0.0, 2.0,
            5.0, -0.5, -5.0, 2.0, 2.0
        ],
        "type": GLfloat
    }
}

data["sphere"] = {
    "vertices": {
        "data": [],
        "type": GLfloat
    },
    "indices": {
        "data": [],
        "type": GLint
    },
    "indices_count": 0
}

# source: http://www.songho.ca/opengl/gl_sphere.html
stack_count = 36
sector_count = 18
stack_step = pi / stack_count
sector_step = 2 * pi / sector_count
radius = 3

for i in range(stack_count + 1):
    stack_angle = pi / 2 - i * stack_step
    xy = radius * cos(stack_angle)
    z = radius * sin(stack_angle)

    k1 = i * (sector_count + 1)
    k2 = k1 + sector_count + 1

    for j in range(sector_count + 1):
        sector_angle = j * sector_step
        x = xy * cos(sector_angle)
        y = xy * sin(sector_angle)

        data["sphere"]["vertices"]["data"] += [*glm.normalize(glm.vec3(x, y, z))]

        if i != 0:
            data["sphere"]["indices"]["data"] += [k1, k2, k1 + 1]

        if i != stack_count - 1:
            data["sphere"]["indices"]["data"] += [k1 + 1, k2, k2 + 1]

        k1 += 1
        k2 += 1

data["sphere"]["indices_count"] = len(data["sphere"]["indices"]["data"])

for k1 in data:
    for k2 in data[k1]:
        if isinstance(data[k1][k2], dict):
            object = data[k1][k2]
            data[k1][k2] = utils.type_cast(object["data"], object["type"])


def get_vertices(name):
    return data[name]["vertices"]


def get_indices(name):
    return data[name]["indices"]


def get_indices_count(name):
    return data[name]["indices_count"]
