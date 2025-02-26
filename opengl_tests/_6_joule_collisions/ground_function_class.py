from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._6_joule_collisions.vbo_stuff import *

import numpy as np

import time

import random


def test():
    #class GroundFunction:
    #    def __init__(self, f_of_x_y, gl_point_size=5):
        #
    #        #self.resolution = 
    #        '''
    #        dist_between_points = (endpoint-startpoint)/num_p + p_size/?
    #        dp - ps/? = (e-s)/n
    #        (e-s)/(dp - ps/?) = n
    #        '''
    #
    #        start_x, start_y, end_x, end_y = -2.6, -2.6, 2.6, 2.6
    #        dist_between_points = 0.0075
    #        unknown_guess = 10**4
    #        g2 = 0.00005
    #        #print(unknown_guess, 3*1/unknown_guess)
    #        num_x = (end_x-start_x)/(dist_between_points - g2/gl_point_size)
    #        num_y = (end_y-start_y)/(dist_between_points - g2/gl_point_size)
    #
    #
    #        #2080 = (2.6-(-2.6))/(0.0028 - 3/10**4)
    #        #5.2/2080 = 0.0028 - 3/10**4
    #
    #        k = (start_x, start_y, end_x, end_y, np.int32(num_x), np.int32(num_y))
    #
    #        print(num_y, num_x)
    #        #raise ValueError(num_y, num_x)
    #
    #
    #        self.data = self.build_function(f_of_x_y, k)
    #
    #        self.vbo = make_vbo(self.data)
    #
    #        self.gl_point_size = gl_point_size
    #
    #
    #    def build_function(self, f_of_x_y, k):
        #
    #        start_x, start_y, end_x, end_y, num_x, num_y = k
    #
    #        x = np.linspace(-2.6, 2.6, num=360)
    #        y = np.linspace(-2.6, 2.6, num=360)
    #        x = np.linspace(start_x, end_x, num=num_x)
    #        y = np.linspace(start_y, end_y, num=num_y)
    #
    #        xy_combos = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)
    #
    #        point_data =  np.array(
    #            (xy_combos[:, 0], xy_combos[:, 1], (f_of_x_y(xy_combos[:, 0], xy_combos[:, 1])))
    #            ).T
    #        
    #
    #        possibilities = np.linspace(0.75, 0.9, num=100)
    #        
    #        L = len(possibilities)
    #        def get_colour():
    #            i = np.random.randint(0, L)
    #            return possibilities[i]
    #
    #        data = np.array([(point[0],
    #                          point[1],
    #                          point[2],
    #                          random.choice(possibilities),
    #                          random.choice(possibilities),
    #                          random.choice(possibilities),
    #                          random.choice(possibilities),
    #                          ) for index, point in enumerate(point_data)]).astype(np.float32)
    #
    #        return data
    pass

class GroundFunction:
    def __init__(self, f_of_x_y):
        self.data = self.build_function(f_of_x_y)

        self.vbo = make_vbo(self.data)


    def build_function(self, f_of_x_y):
        start=time.time()
        x = np.linspace(-2.6, 2.6, num=360)
        y = np.linspace(-2.6, 2.6, num=360)
        #x = np.linspace(-12, 12, num=360)
        #y = np.linspace(-12, 12, num=360)

        xy_combos = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)

        #point_data =  np.array(
        #    (xy_combos[:, 0], xy_combos[:, 1], (-1 * np.cos(xy_combos[:, 0]) * np.cos(xy_combos[:, 1])))
        #    ).T
        #point_data =  np.array(
        #    (xy_combos[:, 0], xy_combos[:, 1], (np.cos(xy_combos[:, 0]) + np.cos(xy_combos[:, 1])))
        #    ).T
        point_data =  np.array(
            (xy_combos[:, 0], xy_combos[:, 1], (f_of_x_y(xy_combos[:, 0], xy_combos[:, 1])))
            ).T
        

        possibilities = np.linspace(0.75, 0.9, num=100)
        
        L = len(possibilities)
        def get_colour():
            i = np.random.randint(0, L)
            return possibilities[i]

        data = np.array([(point[0],
                          point[1],
                          point[2],
                          #np.random.choice(possibilities),
                          #np.random.choice(possibilities),
                          #np.random.choice(possibilities),
                          #np.random.choice(possibilities)
                          random.choice(possibilities),
                          random.choice(possibilities),
                          random.choice(possibilities),
                          random.choice(possibilities),
                          #get_colour(),
                          #get_colour(),
                          #get_colour(),
                          #get_colour(),                         
                          #np.random.random(),
                          #np.random.random(),
                          #np.random.random(),
                          #np.random.random(),
                          ) for index, point in enumerate(point_data)]).astype(np.float32)
        
        #data = point_data.flatten()

        #print(time.time()-start)

        return data
        

#GroundFunction().build_function()