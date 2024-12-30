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
        
        self.width, self.height = 500, 500
        self.aspect_ratio = self.width/self.height

    
    def update_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -self.aspect_ratio * self.zoom,
            self.aspect_ratio * self.zoom,
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


    def build_window(self, window_name="test"):
        
        window = glfw.create_window(self.width, self.height, window_name, None, None)
        glfw.make_context_current(window)
        glfw.get_framebuffer_size(window)
        #self.cursor_key_mouse_callbacks(window)

        return window

    def cursor_key_mouse_callbacks(self, window):
        glfw.set_key_callback(window, self.key_callbacks)
        glfw.set_mouse_button_callback(window, self.mouse_callbacks)
    
    def mouse_callbacks(self, window, mouse_x, mouse_y):
        pass
    
    def key_callbacks(self, window):
        escape = glfw.get_key(window, glfw.KEY_ESCAPE)
        if escape == glfw.PRESS:
            glfw.terminate()

    def main(self):
        if not glfw.init():
            return
        
        window = self.build_window()

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

            glfw.swap_buffers(window)
            glfw.poll_events()