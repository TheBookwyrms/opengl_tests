from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._3_solar_system.object_classes.ellipse_class import *
from opengl_tests._3_solar_system.object_classes.line_of_rotation_class import *
from opengl_tests._3_solar_system.vbo_stuff import *

import numpy as np

class Sphere:
    def __init__(self,
                 radius=1,
                 x_i=0,
                 y_i=0,
                 z_i=0,
                 x_c=[1,0,0],
                 y_c=[0,1,0],
                 z_c=[0,0,1],
                 center=np.array([0, 0, 0]),
                 vec_maj=np.array([10, 0, 0]),
                 vec_min=np.array([0, 10, 0]),
                 e_c=[1, 1, 1],
                 rot_axis_vec =np.array([4, 9.24345, 0]), # vector equivalent to earth's tilt
                 r_axis_c=np.array([1,1,1]),
                 deg_per_rot=1
                 ):
        self.build_sphere_coords(radius, x_i, y_i, z_i, x_c, y_c, z_c)

        ellipse_going_around = Ellipse(center, vec_maj, vec_min, e_c)
        self.e_coords = ellipse_going_around.coords
        self.e_vbo = ellipse_going_around.vbo

        line_of_rotation = LineOfRotation(rot_axis_vec, np.array([x_i, y_i, z_i]), r_axis_c)
        self.l_coords = line_of_rotation.data
        self.l_vbo = line_of_rotation.vbo
        self.r_axis_vec = line_of_rotation.unit_vec
        self.deg_per_rot = deg_per_rot
        self.rad_per_rot = np.radians(deg_per_rot)
        

        self.vbo = make_vbo(self.data)


        self.radius = radius
        self.m = (np.random.randint(3, 8) - np.random.random()) * radius
        self.prev_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.next_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_v = np.array([0, 0, 0], dtype=np.float32)
        self.next_v = np.array([0, 0, 0], dtype=np.float32)
        self.curr_a = np.array([0, 0, 0], dtype=np.float32)
        self.next_a = np.array([0, 0, 0], dtype=np.float32)

        self.trail_s = np.array(([x_i, y_i, z_i, 1, 1, 1],)*512, dtype=np.float32)

        self.trail_vbo = make_vbo(self.trail_s)


    def build_sphere_coords(self, radius, x, y, z, xc, yc, zc):
        heights = np.linspace(0, 2*radius, num=10)
        degrees = np.linspace(0, 360, num=60)
        self.positions = []
        self.colours = []
        for i, h in enumerate(heights):
            h2 = np.abs(h)
            r = np.sqrt(h2*(2*radius-h2))
            for ind, d in enumerate(degrees):
                # x, y, z, r, g, b, a
                x_circ = np.array([
                    r*np.cos(np.radians(d))+x,
                    r*np.sin(np.radians(d))+y,
                    h-radius+z])
                y_circ = np.array([
                    h-radius+x,
                    r*np.cos(np.radians(d))+y,
                    r*np.sin(np.radians(d))+z])
                z_circ = np.array([
                    r*np.cos(np.radians(d))+x,
                    h-radius+y,
                    r*np.sin(np.radians(d))+z])

                self.positions.append(x_circ)
                self.positions.append(y_circ)
                self.positions.append(z_circ)
                self.colours.append([xc[0], xc[1], xc[2]])
                self.colours.append([yc[0], yc[1], yc[2]])
                self.colours.append([zc[0], zc[1], zc[2]])

        vertices = np.array(self.positions, dtype=np.float32)
        self.vertices = vertices
        colours = np.array(self.colours, dtype=np.float32)
        data = np.ones((len(vertices), 6), dtype=np.float32)
        data[:, :3] = vertices
        data[:, 3:] = colours
        self.data = data

    def update_per_ellipse_movement(self, ellipse_data, normal_to_ellipse):
        self.e_coords = np.roll(self.e_coords, shift=1, axis=0)
        normal_to_ellipse = 0

        for i in range(len(self.data)):
            self.data[i, 0] = ellipse_data[0][0] + normal_to_ellipse
            self.data[i, 1] = ellipse_data[0][1] + normal_to_ellipse
            self.data[i, 2] = ellipse_data[0][2] + normal_to_ellipse