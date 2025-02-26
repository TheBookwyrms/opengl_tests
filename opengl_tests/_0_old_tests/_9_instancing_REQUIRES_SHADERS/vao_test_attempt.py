from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def make_vao(data):

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
     
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    n_per_vertice = 3
    n_per_colour = 4
    items_per_point = len(data[0])
    stride = items_per_point*data.itemsize
    

    # enable vertex followed by color within VBOs
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, n_per_vertice, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    # calculate color offset (assuming data is tightly packed)
    # color comes after vertex
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, n_per_colour, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(n_per_vertice * data.itemsize))


    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vao


def vao_draw(point_data, point_vao, draw_type):
    n = point_data.shape[0]

    glBindVertexArray(point_vao)
    
    # draw VBO
    glDrawArrays(draw_type, 0, n)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)