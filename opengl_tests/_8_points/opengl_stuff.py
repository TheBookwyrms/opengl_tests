from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._8_points.vbo_stuff import *

import numpy as np


class OpenGLStuff:
    def __init__(self):
        pass

    def setup(self):


        n = 500

        points_data = np.zeros((n**2, 7))

        x1 = np.linspace(-5, 5, n)
        y1 = np.linspace(-5, 5, n)

        x2, y2 = np.meshgrid(x1, y1)
        x2 = x2.reshape(-1)
        y2 = y2.reshape(-1)

        pm = np.array([x2, y2, np.empty(x2.shape)]).T

        points_data[:, :3] = pm

        self.thetas = np.linspace(0, 2*np.pi, 360)

        f = lambda x, y, a : np.sin(np.cos(x)+a) - np.sin(np.cos(y)-a) # sin/cos wave surface up and down
        g = lambda x, y, a : np.cos(a * np.sqrt(x**2 + y**2)) # concentric circles king of? (but awesome)
        h = lambda x, y, a : np.sqrt(a-x**2-y**2) # dome

        # method 1
        z_s = []
        for t in self.thetas:
            z = f(x2, y2, t)
            z_s.append(z)

        # method 2
        th = self.thetas
        x3, y3, z3 = np.meshgrid(x1, y1, th)
        x3, y3, z3 = x3.reshape(-1), y3.reshape(-1), z3.reshape(-1)
        kz = f(x3, y3, z3).reshape(-1, 360).T


        #self.all_z = kz # method 2
        self.all_z = z_s # method 1
        self.z_num = 0

        
        # r, g, b data
        k = (-1)**np.abs(np.int32(10*points_data[:, :3]))
        points_data[:, 3:6] = k * points_data[:, :3] * 1/5
        
        # opacity data
        points_data[:, 6] = 1

        self.points_data = np.array(points_data).astype(np.float32)
        self.points_vbo = make_vbo(self.points_data)


        self.origin = np.array([0, 0, 0, 1, 1, 1, 1]).astype(np.float32)
        self.origin_vbo = make_vbo(self.origin)


        deg_per_rot = 0.2
        rad_per_rot = np.radians(deg_per_rot)
        theta = rad_per_rot
        self.rotation_matrix = np.array((
                        [np.cos(theta), -np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1],
                        ))


    def rotate_on_axis(self):
        self.points_data[:, :3] = np.matmul(self.points_data[:, :3], self.rotation_matrix)
        pass

    def rotate_colours(self):
        self.points_data[:, 3:6] = np.matmul(self.points_data[:, 3:6], self.rotation_matrix)
        pass


    def update_points(self):
        try:
            self.points_data[:, 2] = self.all_z[self.z_num]
            self.z_num += 1
        except:
            self.z_num = 0
            self.points_data[:, 2] = self.all_z[self.z_num]
            self.z_num += 1


        self.rotate_on_axis()
        #self.rotate_colours()
        update_vbo(self.points_data, self.points_vbo)


    def per_render_loop(self):
        self.update_points()

        draw(self.points_data, self.points_vbo, GL_POINTS, gl_point_size=6)
        draw(self.origin, self.origin_vbo, GL_POINTS, gl_point_size=15)