from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._6_joule_collisions.vbo_stuff import *

import numpy as np


class Normal:
    def __init__(self, x, y, f_of_x_y, df_dx=0, df_dy=0):
        
        # x = red
        # y = green
        # z = blue
        # x, y, z, r, g, b

        f_at_x_y = f_of_x_y(x, y)
        next_x = x+1*df_dx
        next_y = y+1*df_dy
        next_z=f_of_x_y(next_x, next_y)

        #normal = < -df_dx, -df_dy, -1 >

        vertices = np.array([
            [x, y, f_at_x_y, 1.0, 0.0, 0.0, 1.0],
            [x-df_dx, y-df_dy, f_at_x_y+1, 1.0, 0.0, 0.0, 1.0]
        ])


        #vertices = np.array([
        #    [x, y, f_at_x_y, 1.0, 0.0, 0.0, 1.0],
        #    [x+df_dx, y+df_dy, f_at_x_y+next_z, 1.0, 0.0, 0.0, 1.0],
        #])
        #vertices[1] -= (-np.sin(x), -np.sin(y), f_at_x_y, 0, 0, 0, 0)

        self.data = np.array(vertices, dtype=np.float32)

        self.vbo = make_vbo(self.data)


class Gravity:
    def __init__(self, x, y, f_of_x_y):
        vertices=np.array([
            [x, y,   f_of_x_y, 0, 0, 0, 1],
            [x, y, f_of_x_y-2, 0, 0, 0, 1]
        ])

        self.data = np.array(vertices, dtype=np.float32)

        self.vbo = make_vbo(self.data)


class parallel_component_of_gravity:
    def __init__(self, x, y, f_of_x_y, df_dx, df_dy, df):
        f_at_x_y = f_of_x_y(x, y)
        normal_xyz = np.array([df_dx, df_dy, f_at_x_y])/np.linalg.norm([df_dx, df_dy, f_at_x_y])
        #normal_xyz = np.array([df_dx, df_dy, -1])
        gravity = np.array([0, 0, -1])

        component = np.cross(normal_xyz, gravity)

        
        
        a = np.cross(normal_xyz, [df_dx, df_dy, df])
        a=a/np.linalg.norm(a)
        line=a


        #line = (np.dot(gradient, gravity),)*3

        #line = 2*component + np.array([x, y, f_of_x_y])
        #line = np.array([df_dx, df_dy, (f_of_x_y+0.2)])
        #line -= 6*line
        line=(x+line[0], y+line[1], f_at_x_y+line[2])
        line=np.cross(line, normal_xyz)


        next_x = x-1*df_dx
        next_y = y-1*df_dy
        next_z=f_of_x_y(next_x, next_y)
        line = np.array([x-df_dx, y-df_dy, next_z+0])*1
        
        
        line_c = np.array([line[0], line[1], line[2], 0.5, 0.2, 0.8, 1])
        #print(line_c)

        #l2 = np.dot()

        #print(component)

        #parallel = np.array([component[0], component[1], component[2], 0.5, 0.2, 0.8, 1])
        #line_c = parallel

        #print(parallel)

        #parallel -= 5*np.array([component[0], component[1], component[2], 0, 0, 0, 0])

        line1 = np.array([
            [x, y, f_at_x_y, 0.5, 0.2, 0.8, 1],
            line_c,
        ])

        line2 = np.array([
            [x, y, f_at_x_y, 0.5, 0.2, 0.8, 1],
            [x-df_dx, y-df_dy, f_at_x_y-1, 0.5, 0.2, 0.8, 1]
        ])

        parallel_line = (line2)

        ##q = b - ((b*n)/(n*n))
        #q = gravity - (np.dot(gravity, normal_xyz)/np.dot(normal_xyz, normal_xyz))
#
        #parallel_line = np.array([
        #    [x, y, f_at_x_y, 0.5, 0.2, 0.8, 1],
        #    [x+q[0], y+q[1], f_at_x_y+q[2], 0.5, 0.2, 0.8, 1]
        #])
        

        self.data = parallel_line.astype(np.float32)

        self.vbo = make_vbo(self.data)