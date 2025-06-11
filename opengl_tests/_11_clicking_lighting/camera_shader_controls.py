from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import glfw
from glfw.GLFW import *

import numpy as np

import os

import time

from opengl_tests._11_clicking_lighting.matrices import Matrices

class CameraShaders(Matrices):
    def set_initial_values(self):
        super().__init__()

        self.render_distance = 512

        self.width, self.height = 1924, 1080
        #self.width, self.height = 756, 425
        self.aspect_ratio = self.width / self.height

        self.angle_x, self.angle_y, self.angle_z = 12.2, -77.8, 0 # degrees
        self.angle_x, self.angle_y, self.angle_z = 0, 90, 0 # degrees
        self.angle_x, self.angle_y, self.angle_z = 90, -181, 0 # degrees
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0 # degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0 
        self.last_x, self.last_y = 0, 0
        self.zoom = 20

        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01

        self.panning, self.angling = False, False
        self.paused = False
        self.pause_time = time.time()
        self.done = False

        self.background_colour = 0.5, 0.5, 0.5
        #self.background_colour = 0, 0, 0

        self.dt = 0
        self.start = time.time()
        self.current = time.time()



        self.ambient_light_strength = 0.1
        self.ambient_light_colour = np.array([24, 158, 0])/255

        self.light_source_pos = np.array([0, -20, 0], dtype=np.float32) # in world space
        self.light_source_pos = np.array([0, -10, 0], dtype=np.float32) # in world space
        self.light_source_colour = np.array([209, 6, 141])/255

        self.specular_strength = 0.8
        self.specular_power = 2
        self.view_vec = np.array([0, 0, 32, 1]) # ????? NOTE ?????
        
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

    def scroll_callbacks(self, window, xoffset, yoffset):
        if (self.zoom-0.24*yoffset != 0) and not ((self.zoom-0.24*yoffset > -0.1) & (self.zoom-0.24*yoffset < 0.1)):
            self.zoom -= 0.24*yoffset
    
    def mouse_callbacks(self, window, button, action, mods):
        # stops screen panning/rotating if imgui box is moving

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
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                self.pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time()- self.pause_time > 0.01):
                self.paused = False

    def window_size_callbacks(self, window, width, height):
        if not (width==0 or height==0):
            self.width, self.height = width, height
            self.zoom = self.zoom*self.aspect_ratio*self.height/self.width
            self.aspect_ratio = width/height

            glViewport(0, 0, width, height)


    
    def setup_opengl(self):
        self.make_shader_program()

        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    
    def begin_render_actions(self):

        glClearColor(*self.background_colour, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def end_render_actions(self, window):
        
        end = time.time()
        if end-self.current !=0:
            self.dt = end-self.current
        self.current = end
        glfw.swap_buffers(window)
        glfw.poll_events()

    def get_orthographic_projection(self):
        
        (l, r, b, t, n, f) = (-self.aspect_ratio * self.zoom,
                               self.aspect_ratio * self.zoom,
                              -self.zoom,
                               self.zoom,
                              -self.render_distance,
                               self.render_distance)
        orthographic_projection = np.array([
            [2/(r-l), 0, 0, 0],
            [0, 2/(t-b), 0, 0],
            [0, 0, 2/(f-n), 0],
            [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
        ])

        return orthographic_projection
    
    def get_camera_tranform(self):

        camera_rotation = self.rotate_around_p(p=np.array([0,0,0]),
                                               r=(self.angle_x, self.angle_y, self.angle_z))
        camera_pan = self.translate(self.pan_x, self.pan_y, self.pan_z)


        return camera_pan @ camera_rotation

    def get_world_transform(self):

        right_handed = np.array([
            [1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1],])

        world_transform = right_handed
        return world_transform


    def get_vertex_shader_text(self):
        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        vertex_path = lst_f_path.copy()
        vertex_path[-1] = "vertex_shader.glsl"
        vertex_path   = os.sep.join(vertex_path)
        
        with open(vertex_path, "r") as f:
            vertex_shader_text = f.read()
        
        return vertex_shader_text

    def get_object_fragment_shader_text(self):
        
        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        fragment_path = lst_f_path.copy()
        fragment_path[-1] = "object_fragment_shader.glsl"
        fragment_path   = os.sep.join(fragment_path)
        
        with open(fragment_path, "r") as f:
            fragment_shader_text = f.read()
        
        return fragment_shader_text
    
    def get_lighting_fragment_shader_text(self):
        
        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        fragment_path = lst_f_path.copy()
        fragment_path[-1] = "lighting_fragment_shader.glsl"
        fragment_path   = os.sep.join(fragment_path)
        
        with open(fragment_path, "r") as f:
            fragment_shader_text = f.read()
        
        return fragment_shader_text

    def make_shader_program(self):
        vertex_text = self.get_vertex_shader_text()
        vertex_shader = compileShader(vertex_text, GL_VERTEX_SHADER)

        object_fragment_text = self.get_object_fragment_shader_text()
        object_fragment_shader = compileShader(object_fragment_text, GL_FRAGMENT_SHADER)

        lighting_fragment_text = self.get_lighting_fragment_shader_text()
        lighting_fragment_shader = compileShader(lighting_fragment_text, GL_FRAGMENT_SHADER)
        
        self.object_shader_program = compileProgram(vertex_shader, object_fragment_shader, validate=False)
        self.lighting_shader_program = compileProgram(vertex_shader, lighting_fragment_shader, validate=False)

    def set_uniform_float(self, uniform_name, num, shader_program):
        location = glGetUniformLocation(shader_program, uniform_name)
        glUniform1f(location, num)

    def set_uniform_vec3(self, uniform_name, vec3, shader_program):
        location = glGetUniformLocation(shader_program, uniform_name)
        glUniform3fv(location, 1, vec3)

    def set_uniform_mat4(self, uniform_name, mat4, shader_program):
        location = glGetUniformLocation(shader_program, uniform_name)
        glUniformMatrix4fv(location, 1, GL_TRUE, mat4)

    def set_uniforms(self, shader_program):
        self.set_uniform_mat4("world_transform" , self.get_world_transform(), shader_program)
        self.set_uniform_mat4("camera_transform"   , self.get_camera_tranform(), shader_program)
        self.set_uniform_mat4("orthographic_projection", self.get_orthographic_projection(), shader_program)

        self.set_uniform_float("ambient_strength", self.ambient_light_strength, shader_program)
        self.set_uniform_vec3("ambient_colour", self.ambient_light_colour, shader_program)
        self.set_uniform_vec3("light_source_pos", self.light_source_pos, shader_program)
        self.set_uniform_vec3("light_source_colour", self.light_source_colour, shader_program)
        self.set_uniform_float("specular_strength", self.specular_strength, shader_program)
            # camera transform is from origin to camera
            # inv is direction from camera to origin
        inv_cam_transform = np.linalg.inv(self.get_camera_tranform())
        cam_view_pos = np.array(inv_cam_transform @ np.array([1, 1, 1, 1]))[:-1]
        self.set_uniform_vec3("camera_viewpos", cam_view_pos, shader_program)
        self.set_uniform_float("specular_power", self.specular_power, shader_program)
