from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from itertools import combinations

class Cube:
    def __init__(self, center=(0, 0, 0),
                 radius=5,
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
    
def make_vbo(data):
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo

def draw(point_data, point_vbo, draw_type):
    n_per_vertice = 3
    n_per_colour = 3
    stride = point_data.itemsize*7
    n = point_data.shape[0]

    glBindBuffer(GL_ARRAY_BUFFER, point_vbo)

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
    glDrawArrays(draw_type, 0, n)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

if __name__ == "__main__":
    Cube()