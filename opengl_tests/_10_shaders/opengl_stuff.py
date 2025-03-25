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
        sn = [(0, 0, 0), (5, 4, 8)]
        for s in sn:
            cube = Cube(center=s,
                 v_cols=(
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                            (np.random.random(), np.random.random(), np.random.random()),
                         ))
            data = cube.data
            transformation = cube.transformation_matrix
            vao, vbo = make_vao_vbo(data)
            self.instances.append((vao, vbo, data, transformation))



        #cube1 = Cube()
        #self.data = cube1.data
        #self.vao, self.vbo = make_vao_vbo(self.data)

        self.shader_program = make_shaders()



    def per_render_loop(self, window):
        # must draw and perform every other on-loop action

        glUseProgram(self.shader_program)

        for instance in self.instances:
            update_vao_vbo(instance[2], instance[0], instance[1])
            uniforms_v2(self.shader_program, window, instance)
            draw_vao(instance[0], GL_TRIANGLE_STRIP, instance[2].shape[0])

        #make_uniforms(self.shader_program, window, self.data)
        #
        #draw_vao(self.vao, GL_TRIANGLE_STRIP, self.data.shape[0])


