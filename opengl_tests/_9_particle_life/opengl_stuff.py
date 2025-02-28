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

        left, right, top, bottom = -15,10, 20, 5
        left, right, top, bottom = -10, 10, 10, -10
        self.boundary_lines = np.array([
            [left, bottom, 1, 1, 1, 1], [left, top, 1, 1, 1, 1],

            [left, top, 1, 1, 1, 1], [right, top, 1, 1, 1, 1],

            [right, top, 1, 1, 1, 1], [right, bottom, 1, 1, 1, 1],

            [right, bottom, 1, 1, 1, 1], [left, bottom, 1, 1, 1, 1],
        ]).astype(np.float32)
        self.boundary_lines_vbo = make_vbo(self.boundary_lines)
        self.boundary_conditions = np.array([left, right, top, bottom])   




        self.num_partitions = 35
        self.x_blocks = np.linspace(left, right, self.num_partitions, endpoint=False)
        self.y_blocks = np.linspace(bottom, top, self.num_partitions, endpoint=False)
        




        num_points = 150
        rx = np.linspace(left, right, 40)
        ry = np.linspace(bottom, top, 40)
        colours = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
        all_points = []
        for i in range(num_points):
            x, y = np.random.choice(rx), np.random.choice(ry)
            p = Point(x, y, col=np.random.choice(colours))
            all_points.append(p)

        self.all_points = np.array(all_points)



        # set of lines on x[x_blocks], bottom to x[x_blocks], top
        # set of lines on left, y[y_blocks] to right, y[y_blocks]
        
        y_lines = []
        for y in self.y_blocks:
            y_lines.append([left, y, 1, 1, 1, 0.25])
            y_lines.append([right, y, 1, 1, 1, 0.25])

        x_lines = []
        for x in self.x_blocks:

            x_lines.append([x, bottom, 1, 1, 1, 0.25])
            x_lines.append([x, top, 1, 1, 1, 0.25])

        self.y_lines = np.array(y_lines).astype(np.float32)
        self.x_lines = np.array(x_lines).astype(np.float32)

        self.y_vbo, self.x_vbo = make_vbo(self.y_lines), make_vbo(self.x_lines)





    def per_render_loop(self, paused, dt):
        # must draw and perform every other on-loop action
        
        self.num_left = len(self.all_points)

        #a = self.num_partitions-2
        a=1

        for p in self.all_points:
            x_bin = bisect.bisect_left(self.x_blocks, p.data[0])
            y_bin = bisect.bisect_left(self.y_blocks, p.data[1])
            p.grid_square = np.array([x_bin-a, y_bin-a])
            #print(p.grid_square)

        
        grid_per_point = np.array([p.grid_square for p in self.all_points])
                   


        grid = np.empty((self.num_partitions, self.num_partitions), dtype=Point)
        #print(grid)
        for p in self.all_points:
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    xy = np.array([x, y])
                    pgrid = p.grid_square
                    pos = pgrid-xy
                    pos = (pos[0], pos[1])


                    #if pos[0] not in list(range(self.num_partitions)):
                    #    if pos[0] - self.num_partitions in list(range(self.num_partitions)):
                    #        pos = (pos[0] - self.num_partitions, pos[1])
                    #    elif pos[0] + self.num_partitions in list(range(self.num_partitions)):
                    #        pos = (pos[0] + self.num_partitions, pos[1])
                    #        
                    #if pos[1] not in list(range(self.num_partitions)):
                    #    if pos[1] - self.num_partitions in list(range(self.num_partitions)):
                    #        pos = (pos[0], pos[1] - self.num_partitions)
                    #    elif pos[1] + self.num_partitions in list(range(self.num_partitions)):
                    #        pos = (pos[0], pos[1] + self.num_partitions)


                    try:
                        if grid[pos] == None:
                            grid[pos] = [p]
                        else:
                            b = grid[pos]
                            b.append(p)
                            #print(grid[p.grid_square-xy].shape, np.array(b).shape)
                            grid[pos] = b
                    except:
                        pass

                    #if pos in ((2, 4), (2, 5) , (2, 3) ,
                    #             (1, 4) , (1, 5) , (1, 3) ,
                    #             (3, 4) , (3, 5) , (3, 3)):
                    #    print(grid[2, 4], "a")

        #print(grid[2, 4])

        #'''
        #grid_per_point : N long array, containing the grid of point i
        #'''
#
        #cs = np.empty((self.num_partitions**2, self.num_left), dtype=list)
        #xy = 0
        #comparisons = np.empty((len(self.all_points)), dtype=Point)
        #for x in range(self.num_partitions):
        #    for y in range(self.num_partitions):
        #        ''' for each xy pair of the grid '''
#
        #        b = grid_per_point - np.array([x, y])
        #        ''' find distance of each point from x, y '''
#
        #        c = [1 if ((i[0] in [-1, 0, 1]) and (i[1] in [-1, 0, 1])) else 0 for i in b]
        #        ''' if x, y is in the square surrounding point, 1, else 0 '''
#
        #        cs[xy] = np.array(c)
        #        xy += 1
#
        #        for i in range(len(comparisons)):
        #            if c[i] == 1:
        #                ''' if x,y is surrounding point '''
        #                try:
        #                    comparisons[i].append(self.all_points[i])
        #                except:
        #                    comparisons[i] = [self.all_points[i],]
#
#
        ##print(c)
        ##print()
#
        #if not paused:
        #    self.all_points = new_physics_test(self.all_points, grid, dt)
        #    
        #    for i in self.all_points:
        #        i.fix_per_boundary_conditions(i, self.boundary_conditions)
        #        i.vbo = update_vbo(i.data, i.vbo)


        if not paused:
            self.all_points = physics_test_2(self.all_points, grid, dt)
            
            for i in self.all_points:
                i.fix_per_boundary_conditions(i, self.boundary_conditions)
                i.vbo = update_vbo(i.data, i.vbo)



        #for index, grid_tuple in grid_per_point:


        #if not paused:
#
        #    self.all_points = do_physics(self.all_points, dt)
#
        #    for i in self.all_points:
        #        i.fix_per_boundary_conditions(i, self.boundary_conditions)
        #        i.vbo = update_vbo(i.data, i.vbo)

        for i in self.all_points:
            draw(i.data, i.vbo, GL_POINTS, gl_point_size=5)
        
        draw(self.boundary_lines, self.boundary_lines_vbo, GL_LINES)

        draw(self.x_lines, self.x_vbo, GL_LINES, gl_line_width=3)
        draw(self.y_lines, self.y_vbo, GL_LINES, gl_line_width=3)