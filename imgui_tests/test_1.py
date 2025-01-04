import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

import time

class t1:
    def __init__(self):
        self.width, self.height = 1924, 1028
        #self.width, self.height = 481, 257
        self.width, self.height = 600, 500

    def build_window(self, window_name="test"):
        
        window = glfw.create_window(self.width, self.height, window_name, None, None)
        glfw.make_context_current(window)
        glfw.get_framebuffer_size(window)
        self.cursor_key_mouse_callbacks(window)

        
        # initilize imgui context (see documentation)
        imgui.create_context()

        self.imgui_use = GlfwRenderer(window, attach_callbacks=False)

        return window

    def cursor_key_mouse_callbacks(self, window):
        glfw.set_key_callback(window, self.key_callbacks)
    
    def key_callbacks(self, window, key, scancode, action, mods):
        global pause_time
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time()- pause_time > 0.01):
                self.paused = False

    def main(self):
        if not glfw.init():
            return
        
        window = self.build_window()



        glClearColor(0.3, 0.3, 0.3, 1)

       
        self.done = False

        while not self.done:
            glClear(GL_COLOR_BUFFER_BIT)

            # start new frame context
            imgui.new_frame()

            # open new window context
            #imgui.begin("Your first window!", True)

            # draw text label inside of current window
            #imgui.text("Hello world!")
            imgui.begin("Example: child region")

            imgui.begin_child("region", 150, -50, border=True)
            imgui.text("inside region")
            imgui.end_child()

            imgui.text("outside region")# imgui.end()


            # close current window context
            imgui.end()

            # pass all drawing comands to the rendering pipeline
            # and close frame context
            imgui.render()
            self.imgui_use.process_inputs()
            self.imgui_use.render(imgui.get_draw_data())

            glfw.swap_buffers(window)
            glfw.poll_events()



a = t1()
a.main()