import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

from opengl_tests._3_solar_system.object_classes.ellipse_class import *
from opengl_tests._3_solar_system.object_classes.line_of_rotation_class import *
from opengl_tests._3_solar_system.object_classes.sphere_class import *
from opengl_tests._3_solar_system.object_classes.xyz_axis import *
from opengl_tests._3_solar_system.object_classes.background_stars_class import *

from opengl_tests._3_solar_system.celestial_body_classes import *

from opengl_tests._3_solar_system.vbo_stuff import *

from  opengl_tests._3_solar_system.imgui_stuff import *

import time


class SolarSystem:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0 # degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.last_x, self.last_y = 0, 0
        self.zoom = 70    # 185
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

    def main(self, G=0.106743):

        def gen_planets():
            num_b_s = len(self.bodies)
            for b_s in range(num_b_s):
                bh_or_s = self.bodies[b_s]
                self.num_planets = np.random.randint(3, 7)
                #self.num_planets = 1
                pos_range = list(range(-39, 41, 7))
                for i in range(self.num_planets):
                    r = np.random.randint(2, 3)-np.random.random()
                    planet = Planet(
                        radius=r,
                        x_i=np.random.choice(pos_range)+bh_or_s.curr_s[0],
                        y_i=np.random.choice(pos_range)+bh_or_s.curr_s[1],
                        z_i=np.random.choice(pos_range)+bh_or_s.curr_s[2],
                        #x_i=0,
                        #y_i=10,
                        #z_i=0,
                        x_c=[np.random.random(), np.random.random(), np.random.random()],
                        y_c=[np.random.random(), np.random.random(), np.random.random()],
                        z_c=[np.random.random(), np.random.random(), np.random.random()],
                        rot_axis_vec=np.array([np.random.random(), np.random.random(), np.random.random()]),
                        r_axis_c=np.array([1, 1, 1]),
                        deg_per_rot=5
                        )
                    
                    # generates velocity of planet based on velocity required to make
                    # a circular orbit around the black hole, were it only the gravity
                    # of the black hole and no others acting upon it
                    planet.curr_v =np.roll(
                        np.sqrt((
                            (planet.curr_s-bh_or_s.curr_s)**2 * G * bh_or_s.m / (np.linalg.norm(planet.curr_s-bh_or_s.curr_s))**3
                            )),
                        shift=1)
                    
                    self.bodies.append(planet)

        if not glfw.init():
            return
        

        self.imgui_stuff = ImguiStuff()

        window = self.build_window()
        
        self.imgui_stuff.initiate_imgui(window)


        glClearColor(0.05, 0.05, 0.05, 1)
        glEnable(GL_DEPTH_TEST)

        self.bodies = []
        #xyz_axis = axes()

        bkg = BackgroundStars()

        self.bodies = []

        star2 = Star(radius=4,
                               x_i=30,
                               y_i=30,
                               z_i=30)
        #bh_masses = list(range(1600, 2800, 50))
        s_masses = list(range(800, 2400, 50))
        star2.m = np.random.choice(s_masses)
        self.bodies.append(star2)


        star = Star(radius=2,
                    x_i=-30,
                    y_i=-30,
                    z_i=-30)
        s_masses = list(range(800, 2400, 50))
        star.m = np.random.choice(s_masses)
        self.bodies.append(star)

        gen_planets()

        for body in self.bodies:
            theta = body.rad_per_rot
            body.rot_mat = np.array((
                        [np.cos(theta), -np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1]))
            


        dt = 0
        start = time.time()
        current = time.time()

        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()
          
            for p in self.bodies:
                draw(p.data, p.vbo, GL_POINTS) # draws sphere
                
            # force on each planet due to gravity calculations
            for i, planet in enumerate(self.bodies):
                for index, other in enumerate(self.bodies):
                    if planet == other:
                        continue

                    dist_vec = other.curr_s - planet.curr_s
                    dist_vec_mag = np.linalg.norm(dist_vec)

                    if type(other) == Sphere:
                        if dist_vec_mag < 0.5:
                            planet.m += other.m
                            #planet.curr_v += other.curr_v
                            self.bodies.pop(index)
                    elif (type(other) == BlackHole) or (type(other) == Star):
                        if dist_vec_mag < other.radius:
                            other.m += planet.m
                            #planet.curr_v += other.curr_v
                            self.bodies.pop(i)
                        
                    if np.linalg.norm(planet.curr_s) > 1024:
                        self.bodies.pop(i)


                    if planet.m != 0:
                        Fg = G * planet.m * other.m / (dist_vec_mag**2)
                        Fa = dist_vec / dist_vec_mag * Fg
                        planet.next_a += Fa


                # Euler integration
                planet.next_a /= planet.m
                planet.next_v = planet.curr_a * dt + planet.curr_v
                planet.next_s = planet.next_v * dt + planet.curr_s
          
            for p in self.bodies:
                draw(p.vertices, p.vbo, GL_POINTS) # draws sphere
                draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draws trails
                #draw(p.l_coords, p.l_vbo, GL_LINES) # draws line of axis of rotation

                
                if not self.paused:  

                    # updates planet s, v, a per euler integration
                    p.prev_s = p.curr_s
                    p.curr_s = p.next_s
                    p.curr_v = p.next_v
                    p.curr_a = p.next_a

                    # updates trail position based newly previous s
                    p.trail_s = np.roll(p.trail_s, shift=1, axis=0)
                    p.trail_s[0, :3] = p.prev_s[:3]
                    
                    # updates planet s and applies rotation matrix
                    theta = p.rad_per_rot
                    for i in range(len(p.data)):
                        p.data[i, :3] = p.data[i, :3] - p.prev_s + p.curr_s
                        p.data[i, :3] = np.matmul(
                           (p.data[i, :3] - p.curr_s), (p.rot_mat)
                            ) + p.curr_s

                    # resets black holes and stars to their original position
                    if (type(p) == BlackHole) or (type(p) == Star):
                        p.curr_a, p.curr_v, p.curr_s = np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([p.x_i, p.y_i, p.z_i])
                        
                    update_vbo(p)


            self.imgui_stuff.imgui_box(dt, self.bodies, self.paused)
            self.imgui_stuff.render_box()

            #draw(xyz_axis.data, xyz_axis.vbo, GL_LINES) # draws xyz axes
            draw(bkg.data, bkg.vbo, GL_POINTS) # draws background stars
            end = time.time()
            if end-current !=0:
                dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()