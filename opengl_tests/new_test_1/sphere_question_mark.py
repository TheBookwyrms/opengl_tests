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

        #def radius_coords_per_height(radius, height):
        self.positions = []

        def circumferences(r, h):
            degrees = np.linspace(0, 360, num=360)
            for d in degrees:
                x_circ = [r*np.cos(np.radians(d)), r*np.sin(np.radians(d)), h]
                y_circ = [h-radius, r*np.cos(np.radians(d)), r*np.sin(np.radians(d))+radius]
                z_circ = [r*np.cos(np.radians(d)), h-radius, r*np.sin(np.radians(d))+radius]
                self.positions.append(x_circ)
                self.positions.append(y_circ)
                self.positions.append(z_circ)

        def radius_per_height(radius):
            heights = np.linspace(0, 2*radius, num=10)
            for h in heights:
                h2 = np.abs(h)
                r_small = np.sqrt(h2*(2*radius-h2))
                circumferences(r_small, h)
        
        radius_per_height(radius)


        self.vertex_count = len(self.positions)
        vertices = np.array(self.positions, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        vertices.astype(np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 3, ctypes.c_void_p(0))



    def draw(self):
        glBindVertexArray(self.vao)
        glPointSize(4.0)
        glDrawArrays(GL_POINTS, 0, self.vertex_count)