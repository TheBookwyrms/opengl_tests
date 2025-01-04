from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._3_orbiting_rotating_planets.vbo_stuff import *

import numpy as np

class Ellipse:
    def __init__(self,
                 center=np.array([0, 0, 0]),
                 vec_maj=np.array([10, 0, 0]),
                 vec_min=np.array([0, 10, 0]),
                 c=[1, 1, 1]):

        self.build_ellipse_coords(center, vec_maj, vec_min, c)

        self.vbo = make_vbo(self.coords)

    def build_ellipse_coords(self, center, vec_maj, vec_min, c):

        # x(t) = a + cos(t) b + sin(t) c
        # a = center of ellipse
        # b is vector from center to end of major axis
        # c is vector from center to end of minor axis
        # b , c are perpendicular

        degrees = np.linspace(0, 360, num=360)
        self.coords = np.empty((len(degrees), 6), dtype=np.float32)
        for i, d in enumerate(degrees):
            pos = center + np.cos(np.radians(d))*vec_maj + np.sin(np.radians(d))*vec_min
            self.coords[i] = np.array([pos[0], pos[1], pos[2], c[0], c[1], c[2]])