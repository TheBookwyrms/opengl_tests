from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._1_my_the_force_awakens.vbo_and_render import *

class BlackHole:
    def __init__(self, radius=1, x_i=0, y_i=0, z_i=0, x_c=[0,0,0], y_c=[0,0,0], z_c=[0,0,0]):
        self.build_sphere_coords(radius, x_i, y_i, z_i, x_c, y_c, z_c)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


        self.radius = radius
        masses = list(range(800, 2400, 50))
        self.m = np.random.choice(masses)
        self.prev_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.next_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_v = np.array([0, 0, 0], dtype=np.float32)
        self.next_v = np.array([0, 0, 0], dtype=np.float32)
        self.curr_a = np.array([0, 0, 0], dtype=np.float32)
        self.next_a = np.array([0, 0, 0], dtype=np.float32)

        self.trail_s = np.array(([x_i, y_i, z_i, 0, 0, 0],)*2048, dtype=np.float32)
        self.trail_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.trail_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.trail_s.nbytes, self.trail_s, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.stars_s = self.make_stars_s(x_i, y_i, z_i)
        print(self.stars_s, type(self.stars_s), self.stars_s.shape)
        self.stars_vbo = make_vbo(self.stars_s)
        
        theta = np.radians(0.2)
        self.stars_rot_mat = np.array((
                        [np.cos(theta), -np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1],
                        ))



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


    def make_stars_s(self, x, y, z):
        
        n = 2000

        points_data = np.zeros((n, 6))

        # x, y, z data
        multiplier = 5
        m1 = multiplier * (2 * np.random.random((n, 3)) - 1) /2

        x, y, z = 0, 0, 0
        center_point = np.array([x, y, z])
        
        #m2 = 1/np.sinh(np.tan(m1))
        m2 = np.tan(np.cos(m1/0.8)/np.sin(m1*0.05) - 1 )*5 + center_point

        points_data[:, :3] = m2
        
        # r, g, b data
        points_data[:, 3:] = np.array([1, 1, 1])

        a = np.array(points_data).astype(np.float32)
        
        return a



    def update_point_and_trail_vbo(self):

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.data.nbytes, self.data)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindBuffer(GL_ARRAY_BUFFER, self.trail_vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.trail_s.nbytes, self.trail_s)
        glBindBuffer(GL_ARRAY_BUFFER, 0)