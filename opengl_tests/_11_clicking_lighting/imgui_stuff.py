import imgui
from imgui.integrations.glfw import GlfwRenderer

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


class ImguiStuff:
    def in_use(self):
        if self.imgui_use != None and imgui.get_io().want_capture_mouse:
            return True

    def initiate_imgui(self, window, appname):
        self.appname = appname
        imgui.create_context()
        imgui.get_io().display_size = 100,100
        self.imgui_use = GlfwRenderer(window, attach_callbacks=False)

    def imgui_box(self, camera):
        imgui.new_frame()
        imgui.begin(self.appname)

        # dt = 1F / xs
        # 1/x = y/1
        # xy = 1
        # 1/x = y
        # 1/dt = fps
        if not camera.paused:
            if camera.dt != 0:
                imgui.text(f'{1/camera.dt:.2f} fps')
        else:
            imgui.text(f"paused ({1/camera.dt:.2f} fps)")

        imgui.text(f'{camera.angle_x:.1f}, {camera.angle_y:.1f}, {camera.angle_z:.1f} : angles x, y, z')
        imgui.text(f'{camera.pan_x:.2f}  , {camera.pan_y:.2f}  , {camera.pan_z:.2f} : pan x, y, z')
        imgui.text(f'{camera.zoom:.2f} : zoom level')
        imgui.text(f'{camera.aspect_ratio}')

        imgui.end()

    def render_box(self):
        imgui.render()
        self.imgui_use.process_inputs()
        self.imgui_use.render(imgui.get_draw_data())