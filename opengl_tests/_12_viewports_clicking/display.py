from opengl_tests._12_viewports_clicking.window_new import window_new
from opengl_tests._12_viewports_clicking.imgui_stuff import ImguiStuff

from opengl_tests._12_viewports_clicking.shaders import Shaders

from opengl_tests._12_viewports_clicking.base_thing import BaseThing

import time

from OpenGL.GL import *
from OpenGL.GLU import *


class Display:
    def __init__(self):
        pass

    def start_time(self):
        self.dt = 0
        self.current = time.time()

    def time_swaps(self):
        end = time.time()
        if end-self.current !=0:
            self.dt = end-self.current
        self.current = end

    def setup(self):
        pass

        self.width, self.height = 1924, 1080
        self.appname = "_12_ test"




        self.window_class = window_new(self.width, self.height)

        #self.imgui_stuff = ImguiStuff()

        self.window_object = self.window_class.build_window(self.appname) # self.imgui_stuff

        #self.imgui_stuff.initiate_imgui(self.window_object, self.appname)

        self.shaders = Shaders()
        self.shader_program = self.shaders.make_shader_program()

        self.window_class.opengl_initial_setup()

        self.things_list = []

        self.thing_1 = BaseThing()
        self.thing_1.setup(GL_POINTS, (0, 0, self.width//2, self.height))
        self.things_list.append(self.thing_1)


        self.start_time()

        '''
        
        make window
        make appname
        make shaders
        make opengl_stuff
        make imgui
        start time
        
        '''

    def per_render_loop(self):
        self.window_class.begin_loop_actions()

        #self.imgui_stuff.imgui_box(self.window_class)

        if self.window_class.panning or self.window_class.angling or self.window_class.zooming:
            for thing in self.things_list:
                if ((thing.left <= self.window_class.mouse_x <= thing.right) and
                    (thing.bottom <= self.window_class.mouse_y <= thing.top)):
                    thing.panning = self.window_class.panning
                    thing.angling = self.window_class.angling
                    thing.zooming = self.window_class.zooming
                    thing.pan_angle_zoom(self.window_class)

                    thing.panning, thing.angling, thing.zooming = (False,)*3

        glUseProgram(self.shader_program)

        for thing in self.things_list:

            self.shaders.make_uniforms(self.shader_program, self.window_class, thing)

            #if not self.window_class.paused:
            #    self.thing_1.update_thing()

            self.thing_1.draw()

            pass

        self.time_swaps()

        self.window_class.end_loop_actions(self.window_object)


        pass

        '''
        
        begin render loop actions
        imgui
        activate shaders
        draw stuff
        time swaps
        end render loop actions

        '''

    def close_actions(self):
        pass

        # ???

    def main(self):
        self.setup()

        while not self.window_class.done:
            self.per_render_loop()

        self.close_actions()