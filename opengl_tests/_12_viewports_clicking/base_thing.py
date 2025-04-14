from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


class BaseThing:
    def __init__(self):

        self.vao = None
        self.n = None

        self.pan_x, self.pan_y, self.pan_z = (0,)*3
        self.angle_x, self.angle_y, self.angle_z = (0,)*3
        self.zoom = 10

        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01

        self.panning, self.angling, self.zooming = (False,)*3

        pass

    def pan_angle_zoom(self, window):
        if self.panning:
            dx = window.mouse_x - window.last_x
            dy = window.mouse_y - window.last_y
            self.pan_x += dx *    self.pan_sensitivity * self.zoom
            self.pan_y -= dy *    self.pan_sensitivity * self.zoom
            pass

        if self.angling:
            dx = window.mouse_x - window.last_x
            dy = window.mouse_y - window.last_y
            self.angle_x += dy *  self.angle_sensitivity * self.zoom
            self.angle_y += dx *  self.angle_sensitivity * self.zoom
        
            self.angle_x %= 360
            self.angle_y %= 360
            self.angle_z %= 360
            pass

        if self.zooming:
            if (self.zoom-0.24*window.zoom_change != 0) and not (
                    (self.zoom-0.24*window.zoom_change > -0.1) and (self.zoom-0.24*window.zoom_change < 0.1)
                ):
                self.zoom -= 0.24*window.zoom_change
            pass

    def setup(self, draw_type, viewport_dimensions):
        # setup of all elements to be rendered on each loop

        self.set_draw_type(draw_type)
        self.set_viewport(*viewport_dimensions)

        self.data = np.array([
                [0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1]
            ]).astype(np.float32)
        self.vbo, self.vao = self.make_vbo_vao(self.data)
        self.n = self.data.shape[0]

        pass

    def update_thing(self):
        # update elements when necessary

        pass

    def set_draw_type(self, draw_type):
        self.draw_type = draw_type
        
    def set_viewport(self, left, right, bottom, top):
        self.left, self.right = left, right
        self.bottom, self.top = bottom, top

        self.aspect_ratio = (right-left)/(top-bottom)

    def draw(self):
        glViewport(self.left, self.bottom, self.right, self.top)
        if (self.vao != None) and (self.n != None):
            self.draw_vao(self.vao, self.draw_type, self.n)

    def make_vbo_vao(self, data):
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

    def update_vbo_vao(self, data, vbo, vao):
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw_vao(self, vao, draw_type, n):
        glBindVertexArray(vao)
        glPointSize(10)
        glDrawArrays(draw_type, 0, n)
        glBindVertexArray(0)