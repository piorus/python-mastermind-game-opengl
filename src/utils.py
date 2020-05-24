"""
Utility functions used in the application.
"""

import os

import OpenGL.GL as GL
import pygame


def type_cast(what, type_to_cast):
    """
    Cast variable to desired type.

    This is used in the application
    to convert python lists to GLint/GLfloat arrays
    as native python types are not supported out of the box
    as arguments of OpenGL functions.

    :param what: variable to be casted
    :param type_to_cast: type to cast
    :return: variable casted to the type
    """
    return (type_to_cast * len(what))(*what)


# pylint: disable=too-many-arguments
def surface_to_texture(
        surface: pygame.Surface,
        texture: int = None,
        flipped: bool = False,
        wrap_s=GL.GL_REPEAT,
        wrap_t=GL.GL_REPEAT,
        min_filter=GL.GL_LINEAR,
        mag_filter=GL.GL_LINEAR
):
    """
    Convert pygame surface to the OpenGL texture.

    :param surface: pygame Surface object
    :param texture: texture ID where data will be copied
    :param flipped: flip surface data, this is used to handle .png files
    :param wrap_s: GL_TEXTURE_WRAP_S value, default is GL_REPEAT
    :param wrap_t: GL_TEXTURE_WRAP_T value, default is GL_REPEAT
    :param min_filter: GL_TEXTURE_MIN_FILTER value, default is GL_LINEAR
    :param mag_filter: GL_TEXTURE_MAG_FILTER value, default is GL_LINEAR
    :return: ID of the OpenGL texture
    """
    surface_width, surface_height = surface.get_size()
    surface_data = pygame.image.tostring(surface, 'RGBA', flipped)

    texture = texture if texture else GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    # textures - wrapping
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_s)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_t)
    # textures - filtering
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, min_filter)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, mag_filter)
    # textures - load data
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,  # target
        0,  # level
        GL.GL_RGBA,  # internalformat
        surface_width,
        surface_height,
        0,  # border
        GL.GL_RGBA,  # format
        GL.GL_UNSIGNED_BYTE,  # type
        surface_data  # pixels
    )
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    return texture


def load_texture(
        image_path: str,
        wrap_s=GL.GL_REPEAT,
        wrap_t=GL.GL_REPEAT,
        min_filter=GL.GL_LINEAR,
        mag_filter=GL.GL_LINEAR
):
    """
    Load texture from the file.

    :param image_path: path to the texture
    :param wrap_s: GL_TEXTURE_WRAP_S value, default is GL_REPEAT
    :param wrap_t: GL_TEXTURE_WRAP_T value, default is GL_REPEAT
    :param min_filter: GL_TEXTURE_MIN_FILTER value, default is GL_LINEAR
    :param mag_filter: GL_TEXTURE_MAG_FILTER value, default is GL_LINEAR
    :return: ID of the OpenGL texture
    """
    return surface_to_texture(
        surface=pygame.image.load(image_path),
        flipped=os.path.splitext(image_path)[1] != '.png',
        wrap_s=wrap_s,
        wrap_t=wrap_t,
        min_filter=min_filter,
        mag_filter=mag_filter
    )


def list_to_str(combination: list):
    return "".join([str(digit) for digit in combination])