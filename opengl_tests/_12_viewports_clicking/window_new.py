import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import time


class window_new:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.pause_time = time.time()

        self.done = False
        self.paused = False

        self.panning, self.angling, self.zooming = (False,)*3

        self.render_distance = 1024



    def build_window(self, window_name, imgui=None):
        if not glfw.init():
            raise Exception("glfw failed to initialise")
        
        self.imgui = imgui
        
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
        glfw.set_window_size_callback(window, self.window_callbacks)
    
    def window_callbacks(self, window, width, height):
        pass


    '''
    
    for t in things_list:
        if (t.xl <= xpos <= t.xr) and (t.yb <= ypos <= t.yt):
            t is angling/panning/zooming/etc

    thus, each thing class has panning/angling/zooming attributes
        these attributes are put into a translate/rotate/scale matrix
            this is self.camera transform for each thing?
                (or is it world transform?)
    
    '''
    
    def scroll_callbacks(self, window, xoffset, yoffset):
        if yoffset != 0:
            self.zooming = True
            self.zoom_change = yoffset
        else:
            self.zooming = False
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        self.mouse_x, self.mouse_y = xpos, ypos
        
        self.last_x, self.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):
        # stops screen panning/rotating if imgui box is moving
        if self.imgui is not None:
            if self.imgui.in_use():
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
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                self.pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time() - self.pause_time > 0.01):
                self.paused = False

    def opengl_initial_setup(self):
        glClearColor(0.5, 0.5, 0.5, 1)
        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    def begin_loop_actions(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def end_loop_actions(self, window_object):
        glfw.swap_buffers(window_object)
        glfw.poll_events()