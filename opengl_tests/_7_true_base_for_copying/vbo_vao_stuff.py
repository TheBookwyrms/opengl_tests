from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def make_vbo_vao(data):
    n_per_vertice = 3
    n_per_colour = 4
    data_items_per_point = len(data[0])
    data_stride = data_items_per_point*data.itemsize

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, n_per_vertice, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, n_per_colour, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(n_per_vertice * data.itemsize))
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vbo, vao


def update_vbo_vao(data, vbo, vao):
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)


def draw_vao(vao, draw_type, n):
    glBindVertexArray(vao)
    glPointSize(10)
    glDrawArrays(draw_type, 0, n)
    glBindVertexArray(0)