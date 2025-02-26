from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._9_particle_life.vbo_stuff import *
from opengl_tests._9_particle_life.point_class import *
from opengl_tests._9_particle_life.physics import *

import bisect


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def setup(self):
        # setup of all elements to be rendered on each loop

        left, right, top, bottom = -10,10, 10, -10
        self.boundary_lines = np.array([
            [left, bottom, 1, 1, 1, 1], [left, top, 1, 1, 1, 1],

            [left, top, 1, 1, 1, 1], [right, top, 1, 1, 1, 1],

            [right, top, 1, 1, 1, 1], [right, bottom, 1, 1, 1, 1],

            [right, bottom, 1, 1, 1, 1], [left, bottom, 1, 1, 1, 1],
        ]).astype(np.float32)
        self.boundary_lines_vbo = make_vbo(self.boundary_lines)
        self.boundary_conditions = np.array([-10, 10, 10, -10])   


        num_partitions = 7

        self.x_blocks = np.linspace(left, right, num_partitions, endpoint=False)
        self.y_blocks = np.linspace(bottom, top, num_partitions, endpoint=False)
        
        '''p[x, y]'''

        b = np.linspace(-8, 10, 13, endpoint=False)
        print(b)
        place_in_x = []
        for a in b:
            c = bisect.bisect_left(self.x_blocks, a)
            place_in_x.append(self.x_blocks[c-1])
        place_in_x = np.array(place_in_x)
        print(place_in_x)




        num_points = 100
        rx = np.linspace(left, right, 40)
        ry = np.linspace(bottom, top, 40)
        colours = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
        all_points = []
        for i in range(num_points):
            x, y = np.random.choice(rx), np.random.choice(ry)
            p = Point(x, y, col=np.random.choice(colours))
            all_points.append(p)

        self.all_points = np.array(all_points)


    def per_render_loop(self, paused, dt):
        # must draw and perform every other on-loop action
        
        self.num_left = len(self.all_points)


        for p in self.all_points:
            x_bin = bisect.bisect_left(self.x_blocks, p.data[0])
            y_bin = bisect.bisect_left(self.y_blocks, p.data[1])


        if not paused:

            self.all_points = do_physics(self.all_points, dt)

            for i in self.all_points:
                i.fix_per_boundary_conditions(i, self.boundary_conditions)
                i.vbo = update_vbo(i.data, i.vbo)

        for i in self.all_points:
            draw(i.data, i.vbo, GL_POINTS, gl_point_size=5)
        
        draw(self.boundary_lines, self.boundary_lines_vbo, GL_LINES)