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

            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1024, 0.0, 0.0, 1.0]
        ])
        self.data = np.array(vertices, dtype=np.float32)

        self.vertex_count = int(len(self.data)/6)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)