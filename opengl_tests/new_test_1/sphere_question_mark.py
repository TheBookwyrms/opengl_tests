import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import matplotlib.pyplot as plt
import time

class sphere:
    def __init__(self, radius=1):
        pass
        '''
        r = sqrt(x*x + y*y)
        r*r = x*x + y*y

        cos(theta) = x/r
        sin(theta) = y/r

        r**2 = (rcos(theta))**2

        pos = x, y
        pos = sqrt((r/tan(theta))**2 + 1) , sqrt(r**2 - (r/tan(theta))**2 + 1)
        '''
        self.positions = []
        deg = 360
        num_points = 36
        deg_per_point = deg//num_points
        for theta in range(deg//deg_per_point):
            theta*=deg_per_point
            x_pos = radius*np.cos(np.radians(theta))
            y_pos = radius*np.sin(np.radians(theta))
            pos = [np.round(x_pos, 3), np.round(y_pos, 3), 0.0]
            self.positions.append(pos)

        x, y = [], []
        for i in self.positions:
            x.append(i[0])
            y.append(i[1])
        plt.scatter(x, y)
        #plt.show()

        self.vertex_count = len(self.positions)
        vertices = np.array(self.positions, dtype=np.float32)
        print(vertices)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))



    def draw(self):
        glBindVertexArray(self.vao)
        glPointSize(4.0)
        glDrawArrays(GL_POINTS, 0, self.vertex_count)