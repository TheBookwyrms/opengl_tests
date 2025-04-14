from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from itertools import combinations

from opengl_tests._10_shaders.shaders.shaders import *

class Cube:
    def __init__(self, center=(0, 0, 0),
                 radius=1, # half_side_length
                 v_cols=np.zeros((8, 3))):
        self.data = self.make_triangles_of_cube((0, 0, 0), 1, v_cols)

        self.transformation_matrix = translation_rotation_scale_matrix(t=center, s=(radius, radius, radius))

        






    def make_triangles_of_cube(self,
                               center,
                               radius,
                               v_cols):
        

        c0, c1, c2 = center
        r=radius
        vertices = np.array([
            # x, y, z, r, g, b, a
            (c0+r, c1+r, c2+r, v_cols[0][0], v_cols[0][1], v_cols[0][2], 1), # RTF
            (c0+r, c1-r, c2+r, v_cols[1][0], v_cols[1][1], v_cols[1][2], 1), # RBF
            (c0+r, c1+r, c2-r, v_cols[2][0], v_cols[2][1], v_cols[2][2], 1), # RTB
            (c0+r, c1-r, c2-r, v_cols[3][0], v_cols[3][1], v_cols[3][2], 1), # RBB

            (c0-r, c1+r, c2+r, v_cols[4][0], v_cols[4][1], v_cols[4][2], 1), # LTF
            (c0-r, c1-r, c2+r, v_cols[5][0], v_cols[5][1], v_cols[5][2], 1), # LBF
            (c0-r, c1+r, c2-r, v_cols[6][0], v_cols[6][1], v_cols[6][2], 1), # LTB
            (c0-r, c1-r, c2-r, v_cols[7][0], v_cols[7][1], v_cols[7][2], 1), # LBB
        ])

        v = vertices


        #triangles = ((list(combinations(vertices, 4))))
        #triangles = [[tuple(np.float32(comb)) for comb in t] for t in triangles]

        data = np.array([v[1], v[5], v[0], v[4], v[6], v[5], v[7], v[3], v[6], v[2], v[0], v[3], v[1], v[5]]
                         ).astype(np.float32)

        return data