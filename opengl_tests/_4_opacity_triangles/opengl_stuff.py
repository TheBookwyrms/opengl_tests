from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import time


def make_triangle_data():
    data = []
    for i in range(3*np.random.randint(10, 15)):
        data.append([
            np.random.randint(-10, 10),
            np.random.randint(-10, 10),
            np.random.randint(-10, 10),
            np.random.random(),
            np.random.random(),
            np.random.random(),
            np.random.random(),
        ])

    data = np.array(data).astype(np.float32)
    return data

def make_vbo(data):     
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo

def make_triangles():
    data = make_triangle_data()
    vbo = make_vbo(data)
    return data, vbo

def draw(point_data, point_vbo, draw_type):
    n_per_vertice = 3
    n_per_colour = 4
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