from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._5_inside_objects.vbo_stuff import *

from itertools import combinations

class Cube:
    def __init__(self, center=(0, 0, 0),
                 radius=5, # half_side_length
                 v_cols=((np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       (np.random.random(), np.random.random(), np.random.random()),
                                       )):
        self.data = self.make_triangles_of_cube(center, radius, v_cols)

        self.vbo = make_vbo(self.data)

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

        '''
        GL_TRIANGLE_STRIP test:
        RBF, LBF, RTF
             LBF, RTF, LTF
                  RTF, LTF, LTB
                       LTF, LTB, LBF
                            LTB, LBF, LBB
                                 LBF, LBB, RBB,
                                      LBB, RBB, LTB
                                           RBB, LTB, RTB
                                                LTB, RTB, RTF
                                                     RTB, RTF, RBB
                                                          RTF, RBB, RBF
                                                               RBB, RBF, LBF

         RBF,  LBF,  RTF,  LTF,  LTB,  LBF,  LBB,  RBB,  LTB,  RTB,  RTF,  RBB,  RBF,  LBF,
        v[1], v[5], v[0], v[4], v[6], v[5], v[7], v[3], v[6], v[2], v[0], v[3], v[1], v[5],
                                            


        front:
        RBF, LBF, RTF
        LTF, LBF, RTF

        left:
        LTF, LBF, LTB
        LBB, LBF, LTB

        bottom:
        LBB, LBF, RBB
        RBF, LBF, RBB

        right:
        RBF, RBB, RTF
        RTB, RBB, RTF

        back:
        RTB, RBB, LTB
        LBB, RBB, LTB

        top:
        LTF, RTF, LTB
        RTB, RTF, LTB

        '''

        triangles = ((list(combinations(vertices, 4))))
        triangles = [[tuple(np.float32(comb)) for comb in t] for t in triangles]
        #print(triangles)

        data = np.array([v[1], v[5], v[0], v[4], v[6], v[5], v[7], v[3], v[6], v[2], v[0], v[3], v[1], v[5]]
                         ).astype(np.float32)

        return data

if __name__ == "__main__":
    Cube()