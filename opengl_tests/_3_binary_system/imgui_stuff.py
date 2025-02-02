import imgui
from imgui.integrations.glfw import GlfwRenderer

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


class ImguiStuff:
    def __init__(self):
        pass

    def in_use(self):
        if self.imgui_use != None and imgui.get_io().want_capture_mouse:
            return True


    def initiate_imgui(self, window):
        imgui.create_context()
        imgui.get_io().display_size = 100,100
        self.imgui_use = GlfwRenderer(window, attach_callbacks=False)

    def imgui_box(self, dt, bodies, paused):
        imgui.new_frame()
        imgui.begin("Solar System")

        # dt = 1F / xs
        # 1/x = y/1
        # xy = 1
        # 1/x = y
        # 1/dt = fps
        if not paused:
            if dt != 0:
                imgui.text(f'{1/dt:.4g} fps')
        else:
            imgui.text(f"paused ({1/dt:.4g} fps)")


        type_bodies = [str(type(body)) for body in bodies]
        types, counts = np.unique(type_bodies, return_counts=True)

        for i in zip(types, counts):
            words = i[0].split(".")
            imgui.text(f'{i[1]} {i[0].split(".")[3][:-2]}(s)')


        imgui.end()

    def render_box(self):
        imgui.render()
        self.imgui_use.process_inputs()
        self.imgui_use.render(imgui.get_draw_data())