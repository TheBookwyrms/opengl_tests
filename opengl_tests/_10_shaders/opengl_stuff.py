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


        cube1 = Cube()
        self.data = cube1.data

        self.vao, self.vbo = make_vao_vbo(self.data)

        self.shader_program = make_shaders()



    def per_render_loop(self, window):
        # must draw and perform every other on-loop action

        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window, self.data)
        
        draw_vao(self.vao, GL_TRIANGLE_STRIP, self.data.shape[0])


