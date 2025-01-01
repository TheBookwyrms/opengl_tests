import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


class axes:
    def __init__(self):
        
        # x = red
        # y = green
        # z = blue
        # x, y, z, r, g, b
        vertices = np.array([
            [1024, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],

            [0.0, 1024, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],

            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
            [0.0, 0.0, 1024, 0.0, 0.0, 1.0]
        ])
        self.data = np.array(vertices, dtype=np.float32)

        self.vertex_count = int(len(self.data)/6)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def draw(self):
        n_per_vertice = 3
        n_per_colour = 3
        stride = self.data.itemsize*6
        n = 6

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

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
        glDrawArrays(GL_LINES, 0, n)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)