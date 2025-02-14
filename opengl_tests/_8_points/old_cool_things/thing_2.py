from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._8_points.vbo_stuff import *

import numpy as np


class Thing_2:
    def __init__(self):
        pass

    def setup(self):
        
        s = lambda k : np.sin(k)
        c = lambda k : np.cos(k)
        t = lambda k : np.tan(k)
        arr = np.arange(-1, 1, 0.05)

        points = []
        for i in arr:
            for j in arr:
                for k in arr:
                    r, g, b = np.abs(4*i/5), np.abs(4*j/5), np.abs(4*k/5)
                    
                    p = np.array([i, j, k])*5
                    p = np.sin(p)*np.tan(p)

                    p_data = np.array([p[0], p[1], p[2], r, g, b, 1])
                    points.append(p_data)

        self.points_data = np.array(points).astype(np.float32)
        self.points_vbo = make_vbo(self.points_data)

    def per_render_loop(self):
        draw(self.points_data, self.points_vbo, GL_POINTS, gl_point_size=6)