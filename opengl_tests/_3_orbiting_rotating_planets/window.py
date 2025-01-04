import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

from opengl_tests._3_orbiting_rotating_planets.ellipse_class import *
from opengl_tests._3_orbiting_rotating_planets.line_of_rotation_class import *
from opengl_tests._3_orbiting_rotating_planets.sphere_class import *
from opengl_tests._3_orbiting_rotating_planets.vbo_and_render import *
from opengl_tests._3_orbiting_rotating_planets.xyz_axis import *
from opengl_tests._3_orbiting_rotating_planets.background_stars_class import *
from opengl_tests._3_orbiting_rotating_planets.black_hole_class import *

import time


class solar_system:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0 # degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.last_x, self.last_y = 0, 0
        self.zoom = 50    # 185
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
        if self.imgui_use != None and imgui.get_io().want_capture_mouse:
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
            num_b = len(self.bodies)
            for b in range(num_b):
                bh = self.bodies[b]
                num_planets = np.random.randint(3, 7)
                #num_planets = 1
                pos_range = list(range(-39, 41, 7))
                for i in range(num_planets):
                    r = np.random.randint(2, 3)-np.random.random()
                    planet = Sphere(
                        radius=r,
                        x_i=np.random.choice(pos_range)+bh.curr_s[0],
                        y_i=np.random.choice(pos_range)+bh.curr_s[1],
                        z_i=np.random.choice(pos_range)+bh.curr_s[2],
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
                            (planet.curr_s-bh.curr_s)**2 * G * bh.m / (np.linalg.norm(planet.curr_s-bh.curr_s))**3
                            )),
                        shift=1)
                    
                    self.bodies.append(planet)

        if not glfw.init():
            return
        
        window = self.build_window()
        
        imgui.create_context()
        imgui.get_io().display_size = 100,100
        self.imgui_use = GlfwRenderer(window, attach_callbacks=False)

        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)

        self.bodies = []
        xyz_axis = axes()

        bkg = BackgroundStars()

        self.bodies = []

        black_hole = BlackHole(radius=2,
                               x_i=0,
                               y_i=0,
                               z_i=0)
        self.bodies.append(black_hole)

        gen_planets()

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
                #draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draws trails

                
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
                        elif (planet == self.bodies[0]) and (dist_vec_mag > 1024):
                            self.bodies.pop(index)
                    elif type(other) == BlackHole:
                        if dist_vec_mag < other.radius:
                            planet.m += other.m
                            #planet.curr_v += other.curr_v
                            self.bodies.pop(index)
                        elif (planet == self.bodies[0]) and (dist_vec_mag > 1024):
                            self.bodies.pop(index)

                    if planet.m != 0:
                        Fg = G * planet.m * other.m / (dist_vec_mag**2)
                        #print(dist_vec, dist_vec_mag, Fg)
                        Fa = dist_vec / dist_vec_mag * Fg
                        planet.next_a += Fa


                # Euler integration
                planet.next_a /= planet.m
                planet.next_v = planet.curr_a * dt + planet.curr_v
                planet.next_s = planet.next_v * dt + planet.curr_s
          
            for p in self.bodies:
                draw(p.vertices, p.vbo, GL_POINTS) # draws sphere
                draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draws trails
                if type(p) != BlackHole:
                    draw(p.l_coords, p.l_vbo, GL_LINES)
                    #draw(p.e_coords, p.e_vbo, GL_POINTS)

                
                if not self.paused:  

                    # updates planet s, v, a per euler integration
                    p.prev_s = p.curr_s
                    p.curr_s = p.next_s
                    p.curr_v = p.next_v
                    p.curr_a = p.next_a

                    # updates trail position based newly previous s
                    p.trail_s = np.roll(p.trail_s, shift=1, axis=0)
                    p.trail_s[0, :3] = p.prev_s[:3]
                    
                    # updates planet s based on newly previous and current s
                    for i in range(len(p.data)):
                        p.data[i, :3] = p.data[i, :3] - p.prev_s + p.curr_s

                    #rotation of the sphere by angle theta in radians
                    if type(p) != BlackHole:
                       theta = p.rad_per_rot
                       for i in range(len(p.data)):
                           p.data[i, :3] = np.matmul(
                               (p.data[i, :3] - p.curr_s), (np.array((
                                   [np.cos(theta), -np.sin(theta), 0],
                                   [np.sin(theta), np.cos(theta), 0],
                                   [0, 0, 1])))
                           ) + p.curr_s

                    # resets the black hole to the origin (keeps it still)
                    if type(p) == BlackHole:
                        p.curr_a, p.curr_v, p.curr_s = (np.array([0, 0, 0]),)*3

                    # moves the axis line with the planet
                    if type(p) != BlackHole:
                        p.l_coords[0][:3] = p.curr_s + 5*p.r_axis_vec
                        p.l_coords[1][:3] = p.curr_s - 5*p.r_axis_vec
                        
                    p.vbos()

            def imgui_stuff():
                imgui.new_frame()
                imgui.begin("solar system")

                # dt = 1F / xs
                # 1/x = y/1
                # xy = 1
                # 1/x = y
                # 1/dt = fps
                if dt != 0:
                    imgui.text(f'{1/dt} fps')

                imgui.end()


                imgui.render()
                self.imgui_use.process_inputs()
                self.imgui_use.render(imgui.get_draw_data())

            imgui_stuff()

            draw(xyz_axis.data, xyz_axis.vbo, GL_LINES) # draws xyz axes
            draw(bkg.data, bkg.vbo, GL_POINTS) # draws background stars
            end = time.time()
            dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()