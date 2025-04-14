import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

from opengl_tests._12_viewports_clicking.imgui_stuff import *
from opengl_tests._12_viewports_clicking.vbo_vao_stuff import *
from opengl_tests._12_viewports_clicking.opengl_stuff import *

import time



class Window:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def set_initial_values(self):
        self.render_distance = 1024
        
        self.aspect_ratio = self.width/self.height

        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0# degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0 # -39 # self.height/26

        self.last_x, self.last_y = 0, 0
        self.zoom = 5

        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01

        self.panning, self.angling = False, False

    def build_window(self, window_name):
        
        window = glfw.create_window(self.width, self.height, window_name, None, None)
        glfw.make_context_current(window)
        glfw.get_framebuffer_size(window)
        self.cursor_key_mouse_callbacks(window)

        return window

    def cursor_key_mouse_callbacks(self, window):
        glfw.set_key_callback(window, self.key_callbacks)
        glfw.set_mouse_button_callback(window, self.mouse_callbacks)
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callbacks)
        glfw.set_scroll_callback(window, self.scroll_callbacks)
    #    glfw.set_window_size_callback(window, self.window_callbacks)
    #
    #def window_callbacks(self, window, width, height):
    #    if not (width==0 or height==0):
    #        self.width, self.height = width, height
    #        self.zoom = self.zoom*self.aspect_ratio*self.height/self.width
    #        self.aspect_ratio = width/height
    #
    #        glViewport(0, 0, width, height)
    #        # will be changed to double viewport later

    def scroll_callbacks(self, window, xoffset, yoffset):
        if (self.zoom-0.24*yoffset != 0) and not ((self.zoom-0.24*yoffset > -0.1) and (self.zoom-0.24*yoffset < 0.1)):
            self.zoom -= 0.24*yoffset
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        self.mouse_x, self.mouse_y = xpos, ypos
        
        #if self.panning:
        #    dx = xpos - self.last_x
        #    dy = ypos - self.last_y
        #    self.pan_x += dx * self.pan_sensitivity * self.zoom
        #    self.pan_y -= dy * self.pan_sensitivity * self.zoom
        #
        #if self.angling:
        #    dx = xpos - self.last_x
        #    dy = ypos - self.last_y
        #    self.angle_x += dy * self.angle_sensitivity * self.zoom
        #    self.angle_y += dx * self.angle_sensitivity * self.zoom
        #
        #    self.angle_x %= 360
        #    self.angle_y %= 360
        #    self.angle_z %= 360
        
        self.last_x, self.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):
        # stops screen panning/rotating if imgui box is moving
        if self.imgui_stuff.in_use():
            return

        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = True
            elif button == glfw.MOUSE_BUTTON_RIGHT:
                self.angling = True
        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = False
            elif button == glfw.MOUSE_BUTTON_RIGHT:
                self.angling = False
    
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

        self.imgui_stuff = ImguiStuff()

        appname = type(self).__name__
        window = self.build_window(appname)
        
        self.imgui_stuff.initiate_imgui(window, appname)

        
        glClearColor(0.5, 0.5, 0.5, 1)
        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        opengl_stuff_for_window = OpenGLStuff()
        opengl_stuff_for_window.setup()


        self.dt = 0
        current = time.time()

        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            opengl_stuff_for_window.per_render_loop(self)

            self.imgui_stuff.imgui_box(self)
            self.imgui_stuff.render_box()

            end = time.time()
            if end-current !=0:
                self.dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()