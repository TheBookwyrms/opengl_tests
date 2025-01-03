from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


class LineOfRotation:
    def __init__(self, vector_axis, center_pos, c):

        
        self.unit_vec = vector_axis/np.abs(np.linalg.norm(vector_axis))
        begin = center_pos + 5*self.unit_vec
        end = center_pos - 5*self.unit_vec
        
        # x = red
        # y = green
        # z = blue
        # x, y, z, r, g, b
        vertices = np.array([
            [begin[0], begin[1], begin[2], c[0], c[1], c[2]],
            [end[0],     end[1],   end[2], c[0], c[1], c[2]],
        ])
        self.data = np.array(vertices, dtype=np.float32)

        self.vertex_count = int(len(self.data)/6)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)