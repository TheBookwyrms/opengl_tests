import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests.new_test_1.check_key_presses import *
from opengl_tests.new_test_1.objects_on_screen import *
from opengl_tests.new_test_1.from_elsewhere import *
from opengl_tests.new_test_1.sphere_question_mark import *
from opengl_tests.new_test_1.xyz_axis import *
import time

class window_test_with_openGL:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 45 # degrees?
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.last_x, self.last_y = 0, 0
        self.zoom = 45
        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01
        
        self.width, self.height = 1924, 1028
        #self.width, self.height = 481, 257
        #self.width, self.height = 600, 500
        self.aspect_ratio = self.width/self.height

        self.panning, self.angling = False, False

    
    def update_camera(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -self.aspect_ratio * self.zoom,
            self.aspect_ratio * self.zoom,
            -self.zoom,
            self.zoom,
            -1024,
            1024,
        )
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.pan_z)
        matrix = np.array((
            [self.angle_x, 1.0, 0.0, 0.0],
            [self.angle_y, 0.0, 1.0, 0.0],
            [self.angle_z, 0.0, 0.0, 1.0],
            ))
        for i in matrix:
            glRotatef(i[0], i[1], i[2], i[3])


    def build_window(self, window_name="test"):
        
        window = glfw.create_window(self.width, self.height, window_name, None, None)
        glfw.make_context_current(window)
        glfw.get_framebuffer_size(window)
        self.cursor_key_mouse_callbacks(window)

        return window

    def cursor_key_mouse_callbacks(self, window):
        glfw.set_key_callback(window, self.key_callbacks)
        glfw.set_mouse_button_callback(window, self.mouse_callbacks)
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callbacks)
        glfw.set_scroll_callback(window, self.scroll_callbacks)

    def scroll_callbacks(self, window, xoffset, yoffset):
        if self.zoom-yoffset != 0:
            self.zoom -= yoffset
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        if self.panning:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.pan_x += dx * self.pan_sensitivity * self.zoom
            self.pan_y -= dy * self.pan_sensitivity * self.zoom

        if self.angling:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.angle_x += dy * self.angle_sensitivity * self.zoom
            self.angle_y += dx * self.angle_sensitivity * self.zoom

        self.last_x, self.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = True
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
                self.angling = True
        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = False
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
                self.angling = False
    
    def key_callbacks(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True

    

    def main(self, G=1): # G=0.106743
        def planet_maker():
            num_planets = np.random.randint(4, 10)
            for ijk in range(num_planets):
                r = np.random.randint(2, 3)-np.random.random()
                while r <= 0.1:
                    r += 0.2
                pos_range = list(range(-39, 41, 7))
                ijk = sphere(
                    radius=r,
                    x_i=np.random.choice(pos_range),
                    y_i=np.random.choice(pos_range),
                    z_i=np.random.choice(pos_range),
                    )
                ijk.curr_v =np.roll(
                    np.sqrt((
                        (ijk.curr_s-black_hole.curr_s)**2 * G * black_hole.m / (np.linalg.norm(ijk.curr_s-black_hole.curr_s))**3
                        )),
                    shift=1)
                self.planet_renders.append(ijk)


        if not glfw.init():
            return
        
        window = self.build_window()

        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)


        xyz_axis = axes()

        self.planet_renders = []

        black_hole = sphere(radius=2,
                            x_c=[0,0,0],
                            y_c=[0,0,0],
                            z_c=[0,0,0])
        black_hole.m=800
        self.planet_renders.append(black_hole)

        
        planet_maker()

        #circler = sphere(
        #    radius=1,
        #    x_i=8,
        #    y_i=2,
        #    z_i=3
        #)
        #circler.curr_v = np.array([0, np.sqrt(8), 0])
        #self.planet_renders.append(circler)

        '''
        G = 6.67e-7
        G = 1?
        ds**2 * G * M / d**3 = v**2

        (0, 0, 10)**2 * 1 * 80 / 10**3 = v**2
        (0, 0, 8) ? v**2
        (0, 0, np.sqrt(8)) = v
        '''


        
        dt = 0
        start = time.time()
        current = time.time()
        b = "0"

        self.done = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()


            # acceleration calculations
            for i, planet in enumerate(self.planet_renders):
                for index, other in enumerate(self.planet_renders):
                    if planet == other:
                        continue

                    dist_vec = other.curr_s - planet.curr_s
                    dist_vec_mag = np.linalg.norm(dist_vec)

                    if dist_vec_mag < 0.05:
                        planet.m += other.m
                        planet.curr_v += other.curr_v
                        self.planet_renders.pop(index)
                    elif (planet == self.planet_renders[0]) and (dist_vec_mag > 1024):
                        self.planet_renders.pop(index)

                    if planet.m != 0:
                        Fg = G * planet.m * other.m / (dist_vec_mag**2)
                        Fa = dist_vec / dist_vec_mag * Fg
                        planet.next_a += Fa


                # Euler integration
                planet.next_a /= planet.m
                planet.next_v = planet.curr_a * dt + planet.curr_v
                planet.next_s = planet.next_v * dt + planet.curr_s

                # # Verlet integration
                ''' works if no initial velocity, and black hole mass is small '''
                # print(f'prev: {planet.prev_s}, {type(planet.prev_s)}')
                # print(f'current: {planet.curr_s}, {type(planet.curr_s)}')
                # print(f'next: {planet.next_s}, {type(planet.next_s)}')
                # print()
                # planet.next_s = 2*planet.curr_s - planet.prev_s + planet.curr_a * dt**2

            
            for p in self.planet_renders:
                p.draw(p.vertices, p.vbo, GL_POINTS) # draw spheres
                p.draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draw trails

                # updates planet s, v, a per euler integration
                p.prev_s = p.curr_s
                p.curr_s = p.next_s
                p.curr_v = p.next_v
                p.curr_a = p.next_a

                # updates trail position based newly previous s
                p.trail_s = np.roll(p.trail_s, shift=1, axis=0)
                p.trail_s[0][0] = p.prev_s[0]
                p.trail_s[0][1] = p.prev_s[1]
                p.trail_s[0][2] = p.prev_s[2]

                
                # updates planet s based on newly previous and current s
                for i in range(len(p.data)):
                    p.data[i, 0] = p.data[i, 0] - p.prev_s[0] + p.curr_s[0]
                    p.data[i, 1] = p.data[i, 1] - p.prev_s[1] + p.curr_s[1]
                    p.data[i, 2] = p.data[i, 2] - p.prev_s[2] + p.curr_s[2]

                black_hole.curr_a, black_hole.curr_v, black_hole.curr_s = (np.array([0, 0, 0]),)*3

                p.update_point_and_trail_vbo()

            xyz_axis.draw()
            end = time.time()
            dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()