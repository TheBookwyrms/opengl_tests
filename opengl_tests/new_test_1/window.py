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


    def main(self, G=0.106743):
        if not glfw.init():
            return
        
        window = self.build_window()

        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

        xyz_axis = axes()

        planet_renders = []

        black_hole = sphere(radius=2,
                            x_c=[0,0,0],
                            y_c=[0,0,0],
                            z_c=[0,0,0])
        black_hole.m=800
        planet_renders.append(black_hole)

        def planet_maker():
            num_planets = np.random.randint(4, 10)
            for ijk in range(num_planets):
                r = np.random.randint(2, 3)-np.random.random()
                while r <= 0.1:
                    r += 0.2
                pos_range = list(range(-39, 41, 7))
                ijk = sphere(
                    radius=r,
                    #x_i=np.random.randint(-40, 40)-np.random.random(),
                    #y_i=np.random.randint(-40, 40)-np.random.random(),
                    #z_i=np.random.randint(-40, 40)-np.random.random(),
                    x_i=np.random.choice(pos_range),
                    y_i=np.random.choice(pos_range),
                    z_i=np.random.choice(pos_range),
                    )
                #ijk.m *= np.random.randint(1, 5)
                v_s = np.array(list(range(-100, 100, 14)))/100
                ijk.curr_v = np.array([
                     np.random.choice(v_s),
                     np.random.choice(v_s),
                     np.random.choice(v_s),
                ])
                planet_renders.append(ijk)
        planet_maker()
        
        dt = 0
        start = time.time()
        end = 0
        self.done = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()


            # acceleration calculations
            for planet in planet_renders:
                for index, other in enumerate(planet_renders):
                    if planet == other:
                        continue

                    dist_vec = other.curr_s - planet.curr_s
                    dist_vec_mag = np.linalg.norm(dist_vec)

                    if dist_vec_mag < 0.05:
                        planet.m += other.m
                        planet.curr_v += other.curr_v
                        planet_renders.pop(index)

                    if planet.m != 0:
                        Fg = G * planet.m * other.m / (dist_vec_mag**2)
                        Fa = dist_vec / dist_vec_mag * Fg
                        planet.next_a += Fa


                # Euler integration
                planet.next_a /= planet.m
                planet.next_v = planet.curr_a * dt + planet.curr_v
                planet.next_s = planet.next_v * dt + planet.curr_s

                # # Verlet integration
                # print(f'prev: {planet.prev_s}, {type(planet.prev_s)}')
                # print(f'current: {planet.curr_s}, {type(planet.curr_s)}')
                # print(f'next: {planet.next_s}, {type(planet.next_s)}')
                # print()
                # planet.next_s = 2*planet.curr_s - planet.prev_s + planet.curr_a * dt**2

            




            for i in planet_renders:
                i.draw()
                i.prev_s = i.curr_s
                i.curr_s = i.next_s
                i.curr_v = i.next_v
                i.curr_a = i.next_a
                black_hole.curr_a, black_hole.curr_v, black_hole.curr_s = (np.array([0, 0, 0]),)*3
                i.update_vbo()

            xyz_axis.draw()
            end = time.time()
            dt = end-start
            start = end
            glfw.swap_buffers(window)
            glfw.poll_events()