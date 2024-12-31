import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class sphere:
    def __init__(self, radius=1, x_i=0, y_i=0, z_i=0, x_c=[1,0,0], y_c=[0,1,0], z_c=[0,0,1]):
        self.build_sphere_coords(radius, x_i, y_i, z_i, x_c, y_c, z_c)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


        self.radius = radius
        self.m = (np.random.randint(3, 8) - np.random.random()) * radius
        self.prev_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.next_s = np.array([x_i, y_i, z_i], dtype=np.float32)
        self.curr_v = np.array([0, 0, 0], dtype=np.float32)
        self.next_v = np.array([0, 0, 0], dtype=np.float32)
        self.curr_a = np.array([0, 0, 0], dtype=np.float32)
        self.next_a = np.array([0, 0, 0], dtype=np.float32)

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

    def update(self, all_masses, all_positions, velocities, dt, G=1):
        
        '''
        Euler integration:
        mg = fg = GmM/r**2
        g = GM/r**2, M of other planet
        r**2 = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
        a = GM / ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        s2 = s1 + v1t + 0.5at**2
        at+v1 = v2

        Verlet integration:
        mg = fg = GmM/r**2
        g = GM/r**2, M of other planet
        r**2 = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
        x(t+Δt)=2x(t)-x(t-Δt)+a(t)Δt2
        x2 = future, x1 = current, x0 = previous
        x2 = 2x1 - x0 + at**2
        x2 = 2x1 - x0 + (GM / ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))t**2
        '''

        # euler integration / hopefully
        # next pos based on curr v
        # next v based on curr a
        #next a based on gravity


        for i in range(0, len(all_masses)):
            for j in range(0, len(all_masses)):
                if j == i:
                    continue
                s_i, s_j = all_positions[i], all_positions[j]
                m_i, m_j = all_masses[i], all_masses[j]

                ds = s_j-s_i
                d = np.linalg.norm(ds)
                if d < 0.05:
                    d = 0.05
                self.next_a = G * m_j * ds / d**3
                print(self.next_a)

        self.next_v = self.curr_a * dt + self.curr_v
        self.next_s = self.curr_s * dt + self.curr_v
        print(self.curr_s)



        # other_masses = 0
        # other_r_squared = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        # for imp in zip(all_id_s, all_masses, all_positions):
        #     if (imp[0] != self.id) and (imp[0] != 0):
        #         other_masses += imp[1] if imp[1] != self.m else 0
        #         other_r_squared += (imp[2]-self.curr_s)**2 if (imp[2]!=self.curr_s).all() else 0

        # self.next_a = G * other_masses / other_r_squared


        # # my test of verlet integration - hopefully
        # # probably didn't work
        # other_masses = 0
        # other_r_squared = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        # #print(all_id_s, all_masses, all_positions)
        # for imp in zip(all_id_s, all_masses, all_positions):
        #     #print(imp[0], self.id)
        #     if (imp[0] != self.id) and (imp[0] != 0):
        #         other_masses += imp[1] if imp[1] != self.m else 0
        #         other_r_squared += (imp[2]-self.curr_s)**2 if (imp[2]!=self.curr_s).all() else 0

        # self.next_s = 2*self.curr_s - self.prev_s + G*other_masses*dt**2/other_r_squared

    def update_vbo(self):
        for i in range(len(self.data)):
            self.data[i, 0] = self.data[i, 0] - self.prev_s[0] + self.curr_s[0]
            self.data[i, 1] = self.data[i, 1] - self.prev_s[1] + self.curr_s[1]
            self.data[i, 2] = self.data[i, 2] - self.prev_s[2] + self.curr_s[2]

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_DYNAMIC_DRAW)





    def draw(self):
        n_per_vertice = 3
        n_per_colour = 3
        stride = self.vertices.itemsize*6
        n = self.vertices.shape[0]

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # enable vertex followed by color within VBOs
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(n_per_vertice, GL_FLOAT, stride, ctypes.c_void_p(0))
        glEnableClientState(GL_COLOR_ARRAY)

        # calculate color offset (assuming data is tightly packed)
        # color comes after vertex
        size = stride // (n_per_vertice + n_per_colour)
        glColorPointer(n_per_colour, GL_FLOAT, stride, ctypes.c_void_p(n_per_vertice * size))

        # draw VBO
        glPointSize(3)
        glDrawArrays(GL_POINTS, 0, n)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)