import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

def draw(point_data, point_vbo, draw_type):
        n_per_vertice = 3
        n_per_colour = 3
        stride = point_data.itemsize*6
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