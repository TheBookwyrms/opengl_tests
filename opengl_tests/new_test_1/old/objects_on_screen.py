import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def on_screen(window):
    glPointSize(15.0)
    glDrawArrays(GL_POINTS, 0, 5000)
    #test_1()

class test_1:
    def __init__(self):

        self.vertices = np.array((
            0.2, 0.3, 0.4, 0, 1, 0,
            -0.2, -0.3, -0.4, 1, 0, 0,
            0.2, 0.3, 0, 0, 0, 1,
        ), dtype=np.float32)
        self.num_vertices = 3

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glDrawArrays(GL_ARRAY_BUFFER, 0, self.num_vertices)