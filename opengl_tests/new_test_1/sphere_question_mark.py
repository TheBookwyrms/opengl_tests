import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class sphere:
    def __init__(self, radius=1, x_i=0, y_i=0, z_i=0, x_c=[1,0,0], y_c=[0,1,0], z_c=[0,0,1]):
        self.build_sphere_coords(radius, x_i, y_i, z_i, x_c, y_c, z_c)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


        self.radius = radius
        self.m = (np.random.randint(3, 8) - np.random.random()) * radius
        self.prev_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.next_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_v = np.array([0, 0, 0], dtype=np.float32)
        self.next_v = np.array([0, 0, 0], dtype=np.float32)
        self.curr_a = np.array([0, 0, 0], dtype=np.float32)
        self.next_a = np.array([0, 0, 0], dtype=np.float32)

        self.trail_s = np.array(([x_i, y_i, z_i, 1, 1, 1],)*512, dtype=np.float32)
        self.trail_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.trail_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.trail_s.nbytes, self.trail_s, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def build_sphere_coords(self, radius, x, y, z, xc, yc, zc):
        heights = np.linspace(0, 2*radius, num=10)
        degrees = np.linspace(0, 360, num=60)
        self.positions = []
        self.colours = []
        for i, h in enumerate(heights):
            h2 = np.abs(h)
            r = np.sqrt(h2*(2*radius-h2))
            for ind, d in enumerate(degrees):
                # x, y, z, r, g, b, a
                x_circ = np.array([
                    r*np.cos(np.radians(d))+x,
                    r*np.sin(np.radians(d))+y,
                    h-radius+z])
                y_circ = np.array([
                    h-radius+x,
                    r*np.cos(np.radians(d))+y,
                    r*np.sin(np.radians(d))+z])
                z_circ = np.array([
                    r*np.cos(np.radians(d))+x,
                    h-radius+y,
                    r*np.sin(np.radians(d))+z])

                self.positions.append(x_circ)
                self.positions.append(y_circ)
                self.positions.append(z_circ)
                self.colours.append([xc[0], xc[1], xc[2]])
                self.colours.append([yc[0], yc[1], yc[2]])
                self.colours.append([zc[0], zc[1], zc[2]])

        vertices = np.array(self.positions, dtype=np.float32)
        self.vertices = vertices
        colours = np.array(self.colours, dtype=np.float32)
        data = np.ones((len(vertices), 6), dtype=np.float32)
        data[:, :3] = vertices
        data[:, 3:] = colours
        self.data = data

    def update_vbo(self):
        for i in range(len(self.data)):
            self.data[i, 0] = self.data[i, 0] - self.prev_s[0] + self.curr_s[0]
            self.data[i, 1] = self.data[i, 1] - self.prev_s[1] + self.curr_s[1]
            self.data[i, 2] = self.data[i, 2] - self.prev_s[2] + self.curr_s[2]

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)

    def update_trail_vbo(self):
        for i in range(len(self.trail_s)):
            self.trail_s[i, 0] = self.trail_s[i, 0] - self.prev_s[0] + self.curr_s[0]
            self.trail_s[i, 1] = self.trail_s[i, 1] - self.prev_s[1] + self.curr_s[1]
            self.trail_s[i, 2] = self.trail_s[i, 2] - self.prev_s[2] + self.curr_s[2]

        self.trail_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.trail_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.trail_s.nbytes, self.trail_s, GL_DYNAMIC_DRAW)

    def draw_trail(self):
        n_per_vertice = 3
        n_per_colour = 3
        stride = self.trail_s.itemsize*6
        n = self.trail_s.shape[0]

        glBindBuffer(GL_ARRAY_BUFFER, self.trail_vbo)

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
        glDrawArrays(GL_LINE_STRIP, 0, n)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self):
        n_per_vertice = 3
        n_per_colour = 3
        stride = self.vertices.itemsize*6
        n = self.vertices.shape[0]

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
        glDrawArrays(GL_POINTS, 0, n)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)