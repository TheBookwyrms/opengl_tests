import numpy as np

from opengl_tests._9_particle_life.vbo_stuff import *


rgb_table = {
    'black'   : (0, 0, 0),
    'white'   : (1, 1, 1),
    'red'     : (1, 0, 0),
    'green'   : (0, 1, 0),
    'blue'    : (0, 0, 1),
    'yellow'  : (1, 1, 0),
    'magenta' : (1, 0, 1),
    'cyan'    : (0, 1, 1),
}

colours = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan']


class Point:
    def __init__(self, x=0, y=0, col='white'):
        #self.x, self.y = x, y
        self.colour = col

        self.force_to = {}
        for i in colours:
            self.force_to[i] = 2*np.random.random()-1

        self.v = np.array([0, 0]).astype(np.float64)

        data = np.empty((6))
        data[:2] = x, y
        data[2:-1] = rgb_table[self.colour]
        data[-1] = 1

        self.data = np.array(data).astype(np.float32)
        self.vbo = make_vbo(self.data)

        self.grid_square = (None, None)

    def fix_per_boundary_conditions(self, p, boundary_conditions):
        left, right, top, bottom = boundary_conditions
        d_top_bottom = top-bottom
        d_right_left = right-left

        x_good, y_good = (False,)*2

        #p.data[0] %= d_right_left
        ##p.data[0] = p.data[0] - right
        #p.data[1] %= d_top_bottom
        #p.data[0] -= right

        while not x_good:
            if   p.data[0] > right:
                p.data[0] -= d_right_left
            elif p.data[0] < left:
                p.data[0] += d_right_left
            else:
                x_good = True
        
        while not y_good:
            if   p.data[1] > top:
                p.data[1] -= d_top_bottom
            elif p.data[1] < bottom:
                p.data[1] += d_top_bottom
            else:
                y_good = True