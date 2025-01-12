from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def make_vbo(data):
     
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo


def update_vbo(class_instance):
    try:
        glBindBuffer(GL_ARRAY_BUFFER, class_instance.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, class_instance.data.nbytes, class_instance.data)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    except:
        pass
    try:
        glBindBuffer(GL_ARRAY_BUFFER, class_instance.trail_vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, class_instance.trail_s.nbytes, class_instance.trail_s)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    except:
        pass
    try:
        glBindBuffer(GL_ARRAY_BUFFER, class_instance.l_vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, class_instance.l_coords.nbytes, class_instance.l_coords)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    except:
        pass


def draw(point_data, point_vbo, draw_type):
        n_per_vertice = 3
        n_per_colour = 3
        stride = point_data.itemsize*7
        n = point_data.shape[0]

        glBindBuffer(GL_ARRAY_BUFFER, point_vbo)

        # enable vertex followed by color within VBOs
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(n_per_vertice, GL_FLOAT, stride, ctypes.c_void_p(0))
        glEnableClientState(GL_COLOR_ARRAY)

        # calculate color offset (assuming data is tightly packed)
        # color comes after vertex
        size = stride // (n_per_vertice + n_per_colour)
        glColorPointer(n_per_colour, GL_FLOAT, stride, ctypes.c_void_p(n_per_vertice * size))

        # draw VBO
        glPointSize(3)
        glDrawArrays(draw_type, 0, n)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)