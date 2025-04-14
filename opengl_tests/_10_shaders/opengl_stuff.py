from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._10_shaders.make_cube_points import *
from opengl_tests._10_shaders.vbo_vao_stuff import *
from opengl_tests._10_shaders.shaders.shaders import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def setup(self):
        # setup of all elements to be rendered on each loop


        self.instances = []
        k = 5
        i = np.arange(start=-k, stop=k+1, step=3)
        sn = []
        for x in i:
            for y in i:
                for z in i:
                    sn.append((x, y, z))
        #sn = [(0, 0, 0), (5, 4, 8)]
        for s in sn:
            cube = Cube(center=s, v_cols=np.random.random((8, 3)))
            data = cube.data
            transformation = cube.transformation_matrix
            vao, vbo = make_vao_vbo(data)
            self.instances.append((vao, vbo, data, transformation))


        self.shader_program = make_shaders()



    def per_render_loop(self, window):
        # must draw and perform every other on-loop action

        glUseProgram(self.shader_program)

        #glViewport(0, 0, window.width//2, window.height)

        for instance in self.instances:
            update_vao_vbo(instance[2], instance[0], instance[1])
            make_uniforms(self.shader_program, window, instance)
            draw_vao(instance[0], GL_TRIANGLE_STRIP, instance[2].shape[0])

        #glViewport(window.width//2, 0, window.width, window.height)

        #for instance in self.instances:
        #    update_vao_vbo(instance[2], instance[0], instance[1])
        #    make_uniforms(self.shader_program, window, instance)
        #    draw_vao(instance[0], GL_TRIANGLE_STRIP, instance[2].shape[0])
