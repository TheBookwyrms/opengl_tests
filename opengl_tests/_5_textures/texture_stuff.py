from OpenGL.GL import *
from OpenGL.GLU import *

import io
import importlib.resources
from PIL import Image

import numpy as np

from opengl_tests._5_textures.imgui_stuff import *

import time


def make_image_texture(folder, image_path): # folder in format module.folder
    # obtain resource
    bits = importlib.resources.read_binary(folder, image_path)
    image = Image.open(io.BytesIO(bits))

    img_data = image.convert("RGBA").tobytes()
    width, height = image.size

    # bind texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id, width, height


