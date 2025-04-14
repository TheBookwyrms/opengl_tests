from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._11_HEP_display_1.vbo_vao_stuff import *
from opengl_tests._11_HEP_display_1.shaders.shaders import *

from opengl_tests._11_HEP_display_1.scintillator_blocks import *
from opengl_tests._11_HEP_display_1.detection_display import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass


    def setup(self):
        # setup of all elements to be rendered on each loop


        self.scintillator_structuce = ScintillatorStructure()
        self.detected_hulls = DetectionHulls()


        self.shader_program = make_shaders()

        pass

    def per_render_loop(self, window):
        # draw on-loop actions


        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window)


        are_hulls_detected = True
        if are_hulls_detected:
            self.detected_hulls.create_hull_data()
            self.detected_hulls.create_hull_vao()
            self.detected_hulls.draw_hull()

        self.scintillator_structuce.draw_scintillator_structure()


        pass