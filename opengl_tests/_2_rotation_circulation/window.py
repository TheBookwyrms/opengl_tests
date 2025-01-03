import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from opengl_tests._2_rotation_circulation.sphere_class import *
from opengl_tests._2_rotation_circulation.vbo_and_render import *
from opengl_tests._2_rotation_circulation.xyz_axis import *
from opengl_tests._2_rotation_circulation.ellipse_class import *
import time

class rotation_circulation_of_sphere_test:
    def __init__(self):
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0 # degrees
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.last_x, self.last_y = 0, 0
        self.zoom = 8 # 10 # 30    # 185
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
        if not glfw.init():
            return
        
        window = self.build_window()

        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

        self.bodies = []
        xyz_axis = axes()

        self.circulation, self.rotation = (False,)*2


        def create_planet_on_ellipse():
            r = np.random.randint(2, 3)-np.random.random()
            center = np.array([10, 0, 0])
            v_maj = np.array([2, 9, 4])
            v_min = np.array([-15, -6, -7])
            theta_deg = 45
            th_r = np.radians(theta_deg)

            planet = Sphere(
                radius = r,
                x_i = center[0] + np.cos(th_r)*v_maj[0] + np.sin(th_r)*v_min[0],
                y_i = center[1] + np.cos(th_r)*v_maj[1] + np.sin(th_r)*v_min[1],
                z_i = center[2] + np.cos(th_r)*v_maj[2] + np.sin(th_r)*v_min[2],
                x_c = [np.random.random(), np.random.random(), np.random.random()],
                y_c = [np.random.random(), np.random.random(), np.random.random()],
                z_c = [np.random.random(), np.random.random(), np.random.random()],
                center = center,
                vec_maj = v_maj,
                vec_min = v_min,
                e_c = [1, 1, 1]
                )

            self.bodies.append(planet)

            '''
            len(planet.e_coords)//y = theta_deg
            shift = x*theta_deg
            x/y = 3/8

            shift = x * len(planet.e_coords)//y
            8x = 3y
            y = 8x/3
            shift = x * (len(planet.e_coords)//(8x/3))
            shift = 3 * x * (len(planet.e_coords)//8x)
            shift = 3 * (len(planet.e_coords)//8)

            360//y=30
            360/theta_deg = y



            '''

            #   0.5/1 works for theta_deg of  1°
            #   3/8   works for theta_deg of 45°
            #   5/12  works for theta_deg of 30°
            #   1/3   works for theta_deg of 60°
            planet.e_coords = np.roll(planet.e_coords, shift=3*len(planet.e_coords)//8, axis=0)

            self.circulation = True


        def create_rotating_planet():
            r = np.random.randint(2, 3)-np.random.random()
            planet = Sphere(
                radius = r,
                x_i = 0,
                y_i = 0,
                z_i = 0,
                x_c = [np.random.random(), np.random.random(), np.random.random()],
                y_c = [np.random.random(), np.random.random(), np.random.random()],
                z_c = [np.random.random(), np.random.random(), np.random.random()],
                #rot_axis_vec=np.array([90, 0, 0]),
                r_axis_c=np.array([1, 1, 1])
                )

            self.rotation = True


            self.bodies.append(planet)



        #create_planet_on_ellipse()            
        create_rotating_planet()


        dt = 0
        start = time.time()
        current = time.time()

        self.done = False
        self.paused = False

        while not self.done:

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update_camera()
          
            for p in self.bodies:
                draw(p.vertices, p.vbo, GL_POINTS) # draws sphere
                #draw(p.trail_s, p.trail_vbo, GL_LINE_STRIP) # draws trails
                
                if not self.paused:

                    if self.circulation:
                        draw(p.e_coords, p.e_vbo, GL_POINTS)
                        p.e_coords = np.roll(p.e_coords, shift=1, axis=0)                   

                        for i in range(len(p.data)):
                            p.data[i, 0] = p.data[i, 0] - p.e_coords[-1][0] + p.e_coords[0][0]
                            p.data[i, 1] = p.data[i, 1] - p.e_coords[-1][1] + p.e_coords[0][1]
                            p.data[i, 2] = p.data[i, 2] - p.e_coords[-1][2] + p.e_coords[0][2]

                        p.trail_s = np.roll(p.trail_s, shift=1, axis=0)
                        p.trail_s[0][0] = p.curr_s[0]
                        p.trail_s[0][1] = p.curr_s[1]
                        p.trail_s[0][2] = p.curr_s[2]

                        p.update_point_and_trail_vbo()

                    if self.rotation:
                        draw(p.l_coords, p.l_vbo, GL_LINES)


                        theta = p.deg_per_rot
                        for i in range(len(p.data)):
                            p.data[i, :3] = np.matmul(
                                (p.data[i, :3] - p.curr_s), (np.array((
                                    [np.cos(theta), -np.sin(theta), 0],
                                    [np.sin(theta), np.cos(theta), 0],
                                    [0, 0, 1])))
                            ) + p.curr_s


                            #p.data[i, :3] = (p.data[i, :3]*np.cos(theta) +
                            #                np.cross(
                            #                    p.data[i, :3], p.r_axis_vec
                            #                ) * np.sin(theta) +
                            #                p.r_axis_vec * np.dot(
                            #                    p.r_axis_vec, p.data[i, :3]
                            #                    ) * (1-np.cos(theta))
                            #                )
                        
                        
                                # rotation_data =  (p.data[i, :3]*np.cos(theta) +
                                #                 np.cross(
                                #                     p.data[i, :3], p.r_axis_vec
                                #                 ) * np.sin(theta) +
                                #                 p.r_axis_vec * np.dot(p.r_axis_vec, p.data[i, :3]) * (1-np.cos(theta))
                                #                 )

                                # p.data[i, 0] = rotation_data[0]
                                # p.data[i, 1] = rotation_data[1]
                                # p.data[i, 2] = rotation_data[2]

                           
                            p.update_point_and_trail_vbo()


            draw(xyz_axis.data, xyz_axis.vbo, GL_LINES) # draws xyz axes
            end = time.time()
            dt = end-current
            current = end
            glfw.swap_buffers(window)
            glfw.poll_events()