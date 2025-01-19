from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._6_joule_collisions.vbo_stuff import *

import numpy as np

import time

import random

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