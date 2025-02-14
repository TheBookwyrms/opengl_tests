from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._8_points.vbo_stuff import *

import numpy as np


class Thing_1:
    def __init__(self):
        pass

    def setup(self):
        
        t = lambda k : np.tan(k)
        arr = np.arange(-4, 4, 0.2)

        points = []
        for i in arr:
            for j in arr:
                for k in arr:
                    r, g, b = np.abs(i/5), np.abs(j/5), np.abs(k/5)
                    p = np.array([t(i), j, k, r, g, b, 1])
                    points.append(p)

        self.points_data = np.array(points).astype(np.float32)
        self.points_vbo = make_vbo(self.points_data)

    def per_render_loop(self):
        draw(self.points_data, self.points_vbo, GL_POINTS, gl_point_size=6)