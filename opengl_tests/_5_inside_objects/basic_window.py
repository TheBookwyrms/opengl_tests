import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

from opengl_tests._5_inside_objects.imgui_stuff import *
from opengl_tests._5_inside_objects.cube_class import *
#from opengl_tests._5_inside_objects.vbo_stuff import *
from opengl_tests._5_inside_objects.xyz_axis import *

import time



class window_stuff:
    def __init__(self):
        self.render_distance = 1024

        self.angle_x, self.angle_y, self.angle_z = 30, -34, 0 # degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, self.render_distance
        self.last_x, self.last_y = 0, 0
        self.zoom = 15    # 185
        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01 # 0.1 # 0.01
        
        self.width, self.height = 1924, 1028
        #self.width, self.height = 481, 257
        #self.width, self.height = 600, 500
        self.aspect_ratio = self.width/self.height

        self.panning, self.angling, self.z_panning_in, self.z_panning_out = (False,)*4

        self.app_name = str(self).split(".")[-1].split(" ")[0]

    
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


    def build_window(self, window_name="test"):
        
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
        if self.zoom-yoffset != 0:
            self.zoom -= yoffset
    
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
            if key == glfw.KEY_W:
                self.z_panning_in = True
            if key == glfw.KEY_S:
                self.z_panning_out = True
        if action == glfw.RELEASE:
            if key == glfw.KEY_W:
                self.z_panning_in = False
            if key == glfw.KEY_S:
                self.z_panning_out = False

        if self.z_panning_in:
            self.pan_z += 0.5

        if self.z_panning_out:
            self.pan_z -= 0.5

    def main(self):
        if not glfw.init():
            return

        self.imgui_stuff = ImguiStuff()

        window = self.build_window(window_name=self.app_name)
        
        self.imgui_stuff.initiate_imgui(window)

        
        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        self.pan_z += 8

            
        #glEnable(GL_CULL_FACE)
        #glFrontFace(GL_CW)
        #glCullFace(GL_FRONT)
        small_cubes = []

        cube = Cube(center = (-4, -4, -12), radius=10)
        z = -3.5
        for i in range(9):
            x, y = np.random.randint(-5, 5), np.random.randint(-5, 5)
            c = np.random.random()
            individual_cube = Cube(center=(x, y, z), radius=1, v_cols=((c, c, c),)*8)
            z -= 2
            small_cubes.append(individual_cube)
        #cube_small0 = Cube(center=(-4, -4, -15), radius=1, v_cols=((0, 0, 0),)*8)
        #small_cubes.append(cube_small0)
        #cube_small1 = Cube(center=(-1, -1, -17), radius=1, v_cols=((0, 0, 0),)*8)
        #small_cubes.append(cube_small1)
        #cube_small2 = Cube(center=(-8, -8, -18), radius=1, v_cols=((0, 0, 0),)*8)
        #small_cubes.append(cube_small2)
        #cube_small3 = Cube(center=(-4, -4, -13), radius=1, v_cols=((0, 0, 0),)*8)
        #small_cubes.append(cube_small3)
        #cube_small4 = Cube(center=(-4, -4, -11), radius=1, v_cols=((0, 0, 0),)*8)
        #small_cubes.append(cube_small4)

        dt = 0
        start = time.time()
        current = time.time()

        xyz_axis = axes()


        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()

            draw(cube.data, cube.vbo, GL_TRIANGLE_STRIP)
            for i in small_cubes:
                draw(i.data, i.vbo, GL_TRIANGLE_STRIP)
            #draw(cube_small.data, cube_small.vbo, GL_TRIANGLE_STRIP)
            #draw(xyz_axis.data, xyz_axis.vbo, GL_LINES) # draws xyz axes



            self.imgui_stuff.imgui_box(dt, self.paused, app_name=self.app_name)
            self.imgui_stuff.render_box()
            #print(self.angle_x, self.angle_y, self.angle_z)

            end = time.time()
            if end-current !=0:
                dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()