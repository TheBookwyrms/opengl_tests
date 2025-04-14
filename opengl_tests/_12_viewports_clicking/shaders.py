from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram

#import os
#import sys

import numpy as np

class Shaders:
    def __init__(self):
        pass


    def set_mat4_uniform(self, shader_program, uniform_name, mat4):
        uniform_location = glGetUniformLocation(shader_program, uniform_name)
        glUniformMatrix4fv(uniform_location, 1, GL_TRUE, mat4)

    def orthographic_projection(self, left, right, bottom, top, near, far):
        l, r, b, t, n, f = left, right, bottom, top, near, far
        ortho_proj = np.array([
            [     2/(r-l),            0,          0,   0],
            [           0,      2/(t-b),          0,   0],
            [           0,            0,      2/(f-n), 0],
            [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
        ])
        return ortho_proj



    def make_uniforms(self, shader_program, window, thing):

        orthographic_projection = self.orthographic_projection(
                -thing.aspect_ratio * thing.zoom,
                 thing.aspect_ratio * thing.zoom,
                -thing.zoom,
                 thing.zoom,
                -window.render_distance,
                 window.render_distance
            )

        camera_translation = self.translate(thing.pan_x,   thing.pan_y,   thing.pan_z)
        camera_rotation = self.rotate(      thing.angle_x, thing.angle_y, thing.angle_z)

        camera_transformation = camera_translation @ camera_rotation
        inv_cam_transform = np.linalg.inv(camera_transformation)


        identity = np.eye(4)
        right_handed = np.array([
            [1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1],
        ])

        world_transform = identity @ right_handed


        self.set_mat4_uniform(shader_program, "orthographic_projection", orthographic_projection)
        self.set_mat4_uniform(shader_program, "camera_transformation", camera_transformation)
        self.set_mat4_uniform(shader_program, "inv_cam_transform", inv_cam_transform)
        self.set_mat4_uniform(shader_program, "world_transform", world_transform)

    
    def translate(self, x, y, z):
        translation = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])
        
        return translation
    

    def rotate(self, rx, ry, rz):

        rrx, rry, rrz = np.radians(rx), np.radians(ry), np.radians(rz),
        
        rot_x = np.array([
            [1,            0,           0, 0],
            [0,  np.cos(rrx), np.sin(rrx), 0],
            [0, -np.sin(rrx), np.cos(rrx), 0],
            [0,            0,           0, 1]])

        rot_y = np.array([
            [np.cos(rry), 0, -np.sin(rry), 0],
            [          0, 1,            0, 0],
            [np.sin(rry), 0,  np.cos(rry), 0],
            [          0, 0,            0, 1]])

        rot_z = np.array([
            [np.cos(rrz), -np.sin(rrz), 0, 0],
            [np.sin(rrz),  np.cos(rrz), 0, 0],
            [          0,            0, 1, 0],
            [          0,            0, 0, 1],])
        
        return rot_x @ rot_y @ rot_z
    

    def make_vertex_shader(self):
        vertex_shader = '''

        #version 330 core

        layout (location = 0) in vec3 point_pos;
        layout (location = 1) in vec4 point_col;

        out vec4 vertex_colour;

        uniform mat4 orthographic_projection;
        uniform mat4 camera_transformation;
        uniform mat4 inv_cam_transform;
        uniform mat4 world_transform;

        void main() {
            gl_Position = orthographic_projection * camera_transformation *
            world_transform * vec4(point_pos, 1.0);
            vertex_colour = point_col;
        }

        '''

        return vertex_shader
    

    def make_fragment_shader(self):
        fragment_shader = '''

        #version 330 core

        in vec4 vertex_colour;

        out vec4 fragment_colour;

        void main() {
            fragment_colour = vertex_colour;
        }

        '''

        return fragment_shader

    def make_shader_program(self):


        vertex_shader_text   = self.make_vertex_shader()
        fragment_shader_text = self.make_fragment_shader()

        vertex_shader = compileShader(vertex_shader_text, GL_VERTEX_SHADER)

        fragment_shader = compileShader(fragment_shader_text, GL_FRAGMENT_SHADER)
        
        shader_program = compileProgram(vertex_shader, fragment_shader, validate=False)

        return shader_program