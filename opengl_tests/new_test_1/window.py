import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests.new_test_1.check_key_presses import *
from opengl_tests.new_test_1.objects_on_screen import *
from opengl_tests.new_test_1.from_elsewhere import *
from opengl_tests.new_test_1.sphere_question_mark import *

class window_test_with_openGL:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0 # degrees?
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.zoom = 10

    
    def update_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -1 * self.zoom,
            1 * self.zoom,
            -self.zoom,
            self.zoom,
            -1024,
            1024,
        )


        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.pan_z)
        matrix = np.array((
            [self.angle_x, 1.0, 0.0, 0.0],
            [self.angle_y, 0.0, 1.0, 0.0],
            [self.angle_z, 0.0, 0.0, 1.0],
            ))
        for i in matrix:
            glRotatef(i[0], i[1], i[2], i[3])


    def main(self):
        if not glfw.init():
            return
        width, height = 500, 500
        window = glfw.create_window(width, height, "test", None, None)
        glfw.make_context_current(window)

        glfw.get_framebuffer_size(window)

        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)
        test = A()
        test2 = sphere(radius=3)


        while not glfw.window_should_close(window):

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()

            break_loop = check_keys(window)
            if break_loop:
                break

            test2.draw()
            #test.draw()
            #on_screen(window)

            #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glfw.swap_buffers(window)
            glfw.poll_events()