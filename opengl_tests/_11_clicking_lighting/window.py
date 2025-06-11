import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

import time

from opengl_tests._11_clicking_lighting.camera_shader_controls import CameraShaders
from opengl_tests._11_clicking_lighting.imgui_stuff import ImguiStuff
from opengl_tests._11_clicking_lighting.things_to_render import ThingsToRender




class MoreShadersOpenGL:

    def build_window(self, window_name):
        if not glfw.init():
            return
        
        self.window = glfw.create_window(self.camera_shaders.width,
                                    self.camera_shaders.height,
                                    window_name, None, None)
        glfw.make_context_current(self.window)
        glfw.get_framebuffer_size(self.window)
        self.cursor_key_mouse_callbacks(self.window)

    def cursor_key_mouse_callbacks(self, window):
        glfw.set_key_callback(window, self.camera_shaders.key_callbacks)
        glfw.set_mouse_button_callback(window, self.mouse_callbacks)
        glfw.set_cursor_pos_callback(window, self.camera_shaders.cursor_pos_callbacks)
        glfw.set_scroll_callback(window, self.camera_shaders.scroll_callbacks)
        glfw.set_window_size_callback(window, self.camera_shaders.window_size_callbacks)

    def mouse_callbacks(self, window, button, action, mods):
        if self.imgui_stuff.in_use():
            return
        self.camera_shaders.mouse_callbacks(window, button, action, mods)
    


    def main(self):
        self.camera_shaders = CameraShaders()
        self.imgui_stuff = ImguiStuff()
        self.camera_shaders.set_initial_values()

        appname = type(self).__name__
        self.build_window(appname)

        self.camera_shaders.setup_opengl()
        self.imgui_stuff.initiate_imgui(self.window, appname)

        self.things_to_render = ThingsToRender()
        self.things_to_render.setup(self.camera_shaders)

        while not self.camera_shaders.done:
            self.camera_shaders.begin_render_actions()

            self.things_to_render.on_render(self.camera_shaders)

            self.imgui_stuff.imgui_box(self.camera_shaders)
            self.imgui_stuff.render_box()

            self.camera_shaders.end_render_actions(self.window)

        glfw.terminate()