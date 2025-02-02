import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

from opengl_tests._7_true_base_for_copying.imgui_stuff import *

import time



class BaseWindow:
    def __init__(self):
        self.render_distance = 1024
        
        self.width, self.height = 1924, 1028
        #self.width, self.height = 481, 257
        #self.width, self.height = 600, 500
        self.aspect_ratio = self.width/self.height

        #self.angle_x, self.angle_y, self.angle_z = -90, 0, 45 # degrees
        self.angle_x, self.angle_y, self.angle_z = 109, -133, 0 # degrees
        #self.pan_x, self.pan_y, self.pan_z = 109, -133, 0 # -39 # self.height/26
        self.pan_x, self.pan_y, self.pan_z = 0.0488, -1.72, 0 # -39 # self.height/26

        self.angle_x, self.angle_y, self.angle_z = 109+0, -177+0, 0 +90# degrees
        self.pan_x, self.pan_y, self.pan_z = 0.0488, -1.72, 0 # -39 # self.height/26

        #self.angle_x, self.angle_y, self.angle_z = 26.4, -211, 0 # degrees
        #self.pan_x, self.pan_y, self.pan_z = -1.35, 3.87, 0 # -39 # self.height/26

        self.last_x, self.last_y = 0, 0
        self.zoom = 5    # 185
        #self.zoom = 1    # 185
        #self.zoom=0.1
        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01

        self.panning, self.angling = False, False

    
    def update_camera(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -self.aspect_ratio * self.zoom,
            self.aspect_ratio * self.zoom,
            -self.zoom,
            self.zoom,
            -self.render_distance,
            self.render_distance,
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

    def scroll_callbacks(self, window, xoffset, yoffset):
        if (self.zoom-0.24*yoffset != 0) and not ((self.zoom-0.24*yoffset > -0.1) & (self.zoom-0.24*yoffset < 0.1)):
            self.zoom -= 0.24*yoffset
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        if self.panning:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.pan_x += dx * self.pan_sensitivity * self.zoom
            self.pan_y -= dy * self.pan_sensitivity * self.zoom

        if self.angling:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.angle_x += dy * self.angle_sensitivity * self.zoom
            self.angle_y += dx * self.angle_sensitivity * self.zoom

        self.last_x, self.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):
        # stops screen panning/rotating if imgui box is moving
        if self.imgui_stuff.in_use():
            return

        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = True
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
                self.angling = True
        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = False
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
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

        appname = str(type(self)).split(".")[3][:-2]
        window = self.build_window(appname)
        
        self.imgui_stuff.initiate_imgui(window, appname)

        
        glClearColor(0.5, 0.5, 0.5, 1)
        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        #glEnable(GL_MULTISAMPLE)
        #glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)


        dt = 0
        start = time.time()
        current = time.time()

        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()

            self.imgui_stuff.imgui_box(dt, self.paused, self)
            self.imgui_stuff.render_box()

            end = time.time()
            if end-current !=0:
                dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()