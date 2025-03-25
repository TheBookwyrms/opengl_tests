from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram

import os

import numpy as np


def set_mat4_uniform(shader_program, uniform_name, mat4):
    uniform_location = glGetUniformLocation(shader_program, uniform_name)
    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, mat4)




def uniforms_v2(shader_program, window, instance):
    (l, r, b, t, n, f) = (-window.aspect_ratio * window.zoom,
                        window.aspect_ratio * window.zoom,
                        -window.zoom,
                        window.zoom,
                        -window.render_distance,
                        window.render_distance)
    orthographic_projection = np.array([
        [2/(r-l), 0, 0, 0],
        [0, 2/(t-b), 0, 0],
        [0, 0, 2/(f-n), 0],
        [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
    ])


    camera_transformation = translation_rotation_scale_matrix(
        t=(window.pan_x, window.pan_y, window.pan_z),
        r=(window.angle_x, window.angle_y, window.angle_z),
        s=(1, 1, 1))
    
    inv_cam_transform = np.linalg.inv(camera_transformation)


    world_transform = instance[3]


    set_mat4_uniform(shader_program, "orthographic_projection", orthographic_projection)
    set_mat4_uniform(shader_program, "camera_transformation", camera_transformation)
    set_mat4_uniform(shader_program, "inv_cam_transform", inv_cam_transform)
    set_mat4_uniform(shader_program, "world_transform", world_transform)


def translation_rotation_scale_matrix(t=(0, 0, 0), r=(0, 0, 0), s=(1, 1, 1)):
    tx, ty, tz = t
    drx, dry, drz = r # degrees
    rrx, rry, rrz = np.radians(drx), np.radians(dry), np.radians(drz),
    sx, sy, sz = s

    translation = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]])
    
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
    
    scale = np.array([
        [sx,  0,  0, 0],
        [ 0, sy,  0, 0],
        [ 0,  0, sz, 0],
        [ 0,  0,  0, 1]])
    
    transformation_matrix = translation @ scale @ rot_x @ rot_y @ rot_z
    #transformation_matrix = translation @ rot_z @ rot_y @ rot_x

    return transformation_matrix



def make_uniforms(shader_program, window, data):


    # INCREDIBLY useful link for this
    # https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/orthographic-projection-matrix.html
    (l, r, b, t, n, f) = (-window.aspect_ratio * window.zoom,
                        window.aspect_ratio * window.zoom,
                        -window.zoom,
                        window.zoom,
                        -window.render_distance,
                        window.render_distance)
    orthographic_projection = np.array([
        [2/(r-l), 0, 0, 0],
        [0, 2/(t-b), 0, 0],
        [0, 0, 2/(f-n), 0],
        [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
    ])


    # useful for translation and rotation matrices
    # https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html
    translation_matrix = np.array([
        [1, 0, 0, window.pan_x],
        [0, 1, 0, window.pan_y],
        [0, 0, 1, window.pan_z],
        [0, 0, 0, 1]
    ])

    rotation_x_matrix = np.array([
        [1, 0, 0, 0],
        [0,  np.cos(np.radians(window.angle_x)), np.sin(np.radians(window.angle_x)), 0],
        [0, -np.sin(np.radians(window.angle_x)), np.cos(np.radians(window.angle_x)), 0],
        [0, 0, 0, 1]
    ])

    rotation_y_matrix = np.array([
        [np.cos(np.radians(window.angle_y)), 0, -np.sin(np.radians(window.angle_y)), 0],
        [0, 1, 0, 0],
        [np.sin(np.radians(window.angle_y)), 0,  np.cos(np.radians(window.angle_y)), 0],
        [0, 0, 0, 1]
    ])

    rotation_z_matrix = np.array([
        [np.cos(np.radians(window.angle_z)), -np.sin(np.radians(window.angle_z)), 0, 0],
        [np.sin(np.radians(window.angle_z)),  np.cos(np.radians(window.angle_z)), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    # first multiply transformation by x rotation, then that by y rotation
    # as matrix multiplication is non-commutative
    camera_transformation = translation_matrix @ rotation_z_matrix @ rotation_y_matrix @ rotation_x_matrix

    inv_cam_transform = np.linalg.inv(camera_transformation)
    
    #np.matmul(
    #    np.matmul(
    #        np.matmul(translation_matrix, rotation_x_matrix),
    #        rotation_y_matrix
    #        ),
    #    rotation_z_matrix
    #)


    model_transform = np.eye(4) # identity matrix for now, according to Alex




    uniform_location = glGetUniformLocation(shader_program, "inv_cam_transform")
    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, inv_cam_transform)

    uniform_location = glGetUniformLocation(shader_program, "camera_transformation")
    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, camera_transformation)

    uniform_location = glGetUniformLocation(shader_program, "orthographic_projection")
    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, orthographic_projection)

    uniform_location = glGetUniformLocation(shader_program, "model_transform")
    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, model_transform)





    # ambient_strength = 0.2
    # uniform_location = glGetUniformLocation(shader_program, "ambient_strength")
    # glUniform1f(uniform_location, ambient_strength)
# 
    # ambient_light = np.array([0.8, 0.3, 0.55])
    # uniform_location = glGetUniformLocation(shader_program, "ambient_light")
    # glUniform3f(uniform_location, ambient_light[0], ambient_light[1], ambient_light[2])



def make_shaders():

    this_file_path = os.path.abspath(__file__)
    lst_f_path = this_file_path.split("\\")

    vertex_path = lst_f_path.copy()
    fragment_path = lst_f_path.copy()

    vertex_path[-1] = "vertex_shader.glsl"
    fragment_path[-1] = "fragment_shader.glsl"

    vertex_path = "\\".join(vertex_path)
    fragment_path = "\\".join(fragment_path)

    with open(vertex_path, "r") as f:
        vertex_shader_text = f.read()
    vertex_shader = compileShader(vertex_shader_text, GL_VERTEX_SHADER)

    with open(fragment_path, "r") as f:
        fragment_shader_text = f.read()
    fragment_shader = compileShader(fragment_shader_text, GL_FRAGMENT_SHADER)
    
    shader_program = compileProgram(vertex_shader, fragment_shader, validate=False)

    #make_uniforms(shader_program)


    return shader_program