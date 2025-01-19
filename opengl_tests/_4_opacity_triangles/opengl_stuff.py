from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import time


class Triangle:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        coord_1 = np.array([
            np.random.randint(min_x, max_x),
            np.random.randint(min_y, max_y),
            np.random.randint(min_z, max_z),
            np.random.random(),
            np.random.random(),
            np.random.random(),
            np.random.random()])
        coord_2 = np.array([
            np.random.randint(min_x, max_x),
            np.random.randint(min_y, max_y),
            np.random.randint(min_z, max_z),
            np.random.random(),
            np.random.random(),
            np.random.random(),
            np.random.random()])
        coord_3 = np.array([
            np.random.randint(min_x, max_x),
            np.random.randint(min_y, max_y),
            np.random.randint(min_z, max_z),
            np.random.random(),
            np.random.random(),
            np.random.random(),
            np.random.random()])
        
        self.data = np.empty((3, 7), dtype=np.float32)
        self.data[0] = coord_1
        self.data[1] = coord_2
        self.data[2] = coord_3

        self.center = (coord_1[:3] + coord_2[:3] + coord_3[:3])/3

        deg_per_rot = np.array(list(range(int(0.1*100), int(0.5*100), int(0.02*100))))/100
        theta = np.radians(np.random.choice(deg_per_rot))
        self.rot_mat = np.array((
                        [np.cos(theta), -np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1]), dtype=np.float32)
        
        self.vbo = make_vbo(self.data)

def make_vbo(data):     
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo



def make_triangles(min_x=-10,
                   min_y=-10,
                   min_z=-10,
                   max_x= 10,
                   max_y= 10,
                   max_z= 10,):
    triangles = []
    for i in range(np.random.randint(10, 15)):
        triangle = Triangle(min_x, min_y, min_z, max_x, max_y, max_z)
        triangles.append(triangle)

    return triangles


def update(triangle: Triangle):
    triangle.data[:, :3] = np.matmul((triangle.data[:, :3] - triangle.center), (triangle.rot_mat)) + triangle.center
    
    glBindBuffer(GL_ARRAY_BUFFER, triangle.vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, triangle.data.nbytes, triangle.data)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return triangle.data

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