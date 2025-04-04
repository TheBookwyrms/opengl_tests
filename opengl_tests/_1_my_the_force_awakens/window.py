import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._1_my_the_force_awakens.sphere_class import *
from opengl_tests._1_my_the_force_awakens.black_hole_class import *
from opengl_tests._1_my_the_force_awakens.background_stars_class import *
from opengl_tests._1_my_the_force_awakens.vbo_and_render import *
from opengl_tests._1_my_the_force_awakens.xyz_axis import *
from opengl_tests._1_my_the_force_awakens.imgui_stuff import *

import time

from itertools import product

import imgui
from imgui.integrations.glfw import GlfwRenderer

class MyForceAwakens:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 45 # degrees?
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.last_x, self.last_y = 0, 0
        self.zoom = 50 # 185
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
        # stops screen panning/rotating if imgui box is moving
        if self.imgui_stuff.in_use():
            return
        
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
        global pause_time
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time()- pause_time > 0.01):
                self.paused = False

    

    def main(self, G=1): # G=0.106743
        def gen_black_holes():
            num_black_holes = np.random.randint(2, 4)
            for i in range(num_black_holes):
                pos_range = list(range(-200, 200, 13))
                r = np.random.randint(2, 7)-np.random.random()
                black_hole = BlackHole(
                    radius=r,
                    x_i=np.random.choice(pos_range),
                    y_i=np.random.choice(pos_range),
                    z_i=np.random.choice(pos_range),
                )
                self.bodies.append(black_hole)



        def gen_planets():
            num_b = len(self.bodies)
            for b in range(num_b):
                bh = self.bodies[b]
                num_planets = np.random.randint(3, 7)
                #num_planets=50
                pos_range = list(range(-39, 41, 7))
                #pos_range = list(range(-100, 100, 7))
                for i in range(num_planets):
                    r = np.random.randint(2, 3)-np.random.random()
                    planet = Sphere(
                        radius=r,
                        x_i=np.random.choice(pos_range)+bh.curr_s[0],
                        y_i=np.random.choice(pos_range)+bh.curr_s[1],
                        z_i=np.random.choice(pos_range)+bh.curr_s[2],
                        x_c=[np.random.random(), np.random.random(), np.random.random()],
                        y_c=[np.random.random(), np.random.random(), np.random.random()],
                        z_c=[np.random.random(), np.random.random(), np.random.random()],
                        )
                    
                    # generates velocity of planet based on velocity required to make
                    # a circular orbit around the black hole, were it only the gravity
                    # of the black hole and no others acting upon it
                    planet.curr_v =np.roll(
                        np.sqrt((
                            (planet.curr_s-bh.curr_s)**2 * G * bh.m / (np.linalg.norm(planet.curr_s-bh.curr_s))**3
                            )),
                        shift=1)
                    
                    self.bodies.append(planet)
                    self.bodies_dict[planet] = self.num
                    self.num += 1


        if not glfw.init():
            return
        

        self.imgui_stuff = ImguiStuff()

        window = self.build_window()
        
        self.imgui_stuff.initiate_imgui(window)


        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)


        # xyz_axis = axes()
        bkg = BackgroundStars()

        self.bodies = []
        self.bodies_dict = {}
        self.num = 0

        black_hole = BlackHole(radius=2,
                               x_i=0,
                               y_i=0,
                               z_i=0)
        self.bodies.append(black_hole)
        self.bodies_dict[black_hole] = self.num
        self.num += 1


        # gen_black_holes()
        gen_planets()

        
        dt = 0
        start = time.time()
        current = time.time()

        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()

            '''tests from _3_binary_system'''
            def tests_to_ignore():
                #            def ignore():
                #                import numpy as np
                #                from itertools import combinations
                #                from itertools import product
                #
                #                a = np.array([0, 1, 2, 3, 4, 5])
                #
                #                G=1
                #                g = (lambda mass, pos_1, pos_2 :
                #                        G * mass * (pos_1-pos_2) / np.linalg.norm(pos_1-pos_2)**3
                #                        if np.linalg.norm(pos_1-pos_2) != 0 else 0)
                #
                #                b = np.empty((len(a), len(a)))
                #
                #                c = product(a, a)
                #                c = [e for e in c]
                #
                #                for e in c:
                #                    b[e[0], e[1]] = float(f'{g(1, e[0], e[1]):.3f}')
                #                    
                #                print(b)
                #                d = np.add.reduce(b)
                #                print(d)
                #
                #
                #            for i, planet in enumerate(self.bodies):
                #                for index, other in enumerate(self.bodies):
                #                    if planet == other:
                #                        continue
                #                    dist_mag = np.linalg.norm(other.curr_s - planet.curr_s)
                #                    if dist_mag < 0.5:
                #                        planet.m += other.m
                #                        #planet.curr_v += other.curr_v
                #                        self.bodies.pop(index)
                #                    if (planet == self.bodies[0]) and (dist_mag > 1024):
                #                        self.bodies.pop(index)
                #
                #            Fg = (lambda mass_1, mass_2, pos_1, pos_2 :
                #                    mass_1 * mass_2 * (pos_1-pos_2) / np.linalg.norm(pos_1-pos_2)**3
                #                    if np.linalg.norm(pos_1-pos_2) != 0 else 0)
                #
                #            num_bodies = len(self.bodies)
                #            list_num_bodies = range(num_bodies)
                #            interactions = np.empty((num_bodies, num_bodies), dtype=np.ndarray)
                #            box_combinations = product(list_num_bodies, list_num_bodies)
                #            box_combinations = [b for b in box_combinations]
                #
                #            for combination in box_combinations:
                #                interactions[combination[0], combination[1]] = (
                #                    Fg(self.bodies[combination[0]].m,
                #                      self.bodies[combination[1]].m,
                #                      self.bodies[combination[0]].curr_s,
                #                      self.bodies[combination[1]].curr_s,)
                #                )
                #
                #            Fg_per_planet = np.add.reduce(interactions)
                #
                #            for index, planet in enumerate(self.bodies):
                #                planet.next_a = G*Fg_per_planet[index]/planet.m
                #                planet.next_v = planet.curr_a * dt + planet.curr_v
                #                planet.next_s = planet.next_v * dt + planet.curr_s
                #
                #            
                #            def ignore_2():
                #                pass
                #                g = np.array([0, 0, 0], dtype=np.float32)
                #                for planet in self.bodies:
                #                    if planet != self.bodies[0]:
                #                        pass
                #                        pos = planet.curr_s
                #                        mag_pos = np.linalg.norm(pos)
                #
                #                        g_vec = (planet.m * pos) / mag_pos**3
                #
                #                        g += g_vec
                #                    #else:
                #                    #    g -= (planet.m,)*3
                #                g *= G
                #
                #                for planet in self.bodies:
                #                    if planet != self.bodies[0]:
                #                        pos = planet.curr_s
                #                        mag_pos = np.linalg.norm(pos)
                #
                #                        g_vec = (planet.m * pos) / mag_pos**3
                #
                #                        planet.next_a = g - (G*g_vec)
                #                        planet.next_v = planet.curr_a * dt + planet.curr_v
                #                        planet.next_s = planet.next_v * dt + planet.curr_s
                pass


            # force on each planet due to gravity calculations
            for i, planet in enumerate(self.bodies):
                next_a = np.array([0, 0, 0], dtype=np.float64)
                for index, other in enumerate(self.bodies):
                    if planet == other:
                        continue
                    dist_vec = other.curr_s - planet.curr_s
                    dist_vec_mag = np.linalg.norm(dist_vec)
                    unit_dist_vec = dist_vec/dist_vec_mag
                    if dist_vec_mag < 0.5:
                        planet.m += other.m
                        #planet.curr_v += other.curr_v
                        self.bodies.pop(index)
                    elif (planet == self.bodies[0]) and (dist_vec_mag > 1024):
                        self.bodies.pop(index)
                    if planet.m != 0:
                        pass
                        #g = G * other.m / (dist_vec_mag**2)
                        #a = dist_vec / dist_vec_mag * g

                        #a = dist_vec * G * other.m / dist_vec_mag**3
                        a = G * other.m / dist_vec_mag**2 * unit_dist_vec
                        next_a += a

#                # Euler integration
                planet.next_a = next_a
                planet.next_v = planet.curr_a * dt + planet.curr_v
                planet.next_s = planet.next_v * dt + planet.curr_s
          
            for p in self.bodies:
                draw(p.vertices, p.vbo, GL_POINTS) # draws sphere
                draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draws trails
                
                if not self.paused:  

                    # updates planet s, v, a per euler integration
                    if p != self.bodies[0]:
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


                    p.update_point_and_trail_vbo()

                    if type(p) == BlackHole:
                        #draw(p.stars_s, p.stars_vbo, GL_POINTS)
                        #p.stars_s[:, :3] = np.matmul(p.stars_s[:, :3], p.stars_rot_mat)
                        #p.stars_vbo = update_vbo(p.stars_s, p.stars_vbo)
                        pass

            
            self.imgui_stuff.imgui_box(dt, self.bodies, self.paused)
            self.imgui_stuff.render_box()


            # draw(xyz_axis.data, xyz_axis.vbo, GL_LINES) # draws xyz axes
            draw(bkg.vertices, bkg.vbo, GL_POINTS) # draws background stars
            end = time.time()
            dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()