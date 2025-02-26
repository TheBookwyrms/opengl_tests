from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._0_old_tests._9_instancing_REQUIRES_SHADERS.make_cube_points import *
from opengl_tests._0_old_tests._9_instancing_REQUIRES_SHADERS.vbo_stuff import *
from opengl_tests._0_old_tests._9_instancing_REQUIRES_SHADERS.vao_test_attempt import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def setup(self):
        # setup of all elements to be rendered on each loop

        self.translations = np.empty((64, 3)).astype(np.float32)
        k=0
        for z in range(-10, 10, 5):
            for y in range(-10, 10, 5):
                for x in range(-10, 10, 5):
                    self.translations[k]=np.array([x/10.1, y/10.1, z/10.1])
                    k += 1

        cube1 = Cube()
        self.data = cube1.data
        #self.cube_1_data = self.data


        instance_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.translations.nbytes, self.translations, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)



        n_per_vertice = 3
        n_per_colour = 4
        data_items_per_point = len(self.data[0])
        data_stride = data_items_per_point*self.data.itemsize

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, n_per_vertice, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, n_per_colour, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(n_per_vertice * self.data.itemsize))
        
        translations_items_per_point = len(self.data[0])
        translations_stride = translations_items_per_point*self.translations.itemsize
        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
        glVertexAttribPointer(2, self.translations.shape[1], GL_FLOAT, GL_FALSE, translations_stride, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glVertexAttribDivisor(2, 1)

        glBindVertexArray(0)

        #self.cube_1_vao = make_vao(self.cube_1_data)


    def per_render_loop(self):
        # must draw and perform every other on-loop action
        glBindVertexArray(self.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.data.shape[0], self.translations.shape[0])
        glBindVertexArray(0)
        #vao_draw(self.cube_1_data, self.cube_1_vao, GL_TRIANGLES)