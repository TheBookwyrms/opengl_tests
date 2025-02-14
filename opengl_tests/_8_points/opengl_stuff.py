from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._8_points.vbo_stuff import *

import numpy as np


class OpenGLStuff:
    def __init__(self):
        pass

    def setup(self):
        
        n = 5000

        points_data = np.zeros((n, 7))

        # x, y, z data
        multiplier = 5
        m1 = multiplier * (2 * np.random.random((n, 3)) - 1) /2
        
        m2 = np.sin(m1)
        #m2 = 1/np.sin(m1)
        #m2 = np.sinh(m1)
        #m2 = 1/np.sinh(np.tan(m1))

        points_data[:, :3] = m2
        
        # r, g, b data
        k = (-1)**np.abs(np.int32(10*points_data[:, :3]))
        points_data[:, 3:6] = k * points_data[:, :3] * 4/5
        
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
        #self.rotate_on_axis()
        self.rotate_colours()
        update_vbo(self.points_data, self.points_vbo)


    def per_render_loop(self):
        self.update_points()

        draw(self.points_data, self.points_vbo, GL_POINTS, gl_point_size=6)
        draw(self.origin, self.origin_vbo, GL_POINTS, gl_point_size=15)