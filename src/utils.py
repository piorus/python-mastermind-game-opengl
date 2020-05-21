import pygame, os
from OpenGL.GL import *


def type_cast(what, type):
    return (type * len(what))(*what)


def surface_to_texture(
        surface,
        texture: int = None,
        flipped: bool = False,
        wrap_s=GL_REPEAT,
        wrap_t=GL_REPEAT,
        min_filter=GL_LINEAR,
        mag_filter=GL_LINEAR
):
    surface_width, surface_height = surface.get_size()
    surface_data = pygame.image.tostring(surface, 'RGBA', flipped)

    texture = texture if texture else glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # textures - wrapping
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
    # textures - filtering
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, mag_filter)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        surface_width,
        surface_height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        surface_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture


def load_texture(image_path, wrap_s=GL_REPEAT, wrap_t=GL_REPEAT, min_filter=GL_LINEAR, mag_filter=GL_LINEAR):
    return surface_to_texture(
        pygame.image.load(image_path),
        flipped=os.path.splitext(image_path)[1] != '.png',
        wrap_s=wrap_s,
        wrap_t=wrap_t,
        min_filter=min_filter,
        mag_filter=mag_filter
    )
