import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_tests._11_clicking_lighting.vao_vbo import create_vao, update_vbo, draw_vao
from opengl_tests._11_clicking_lighting.matrices import Matrices

import time

class ThingsToRender:
    def setup(self, shaders):


        def iterate_square(two_triangles, n_subdivisions):
            def make_n_subdivisions(triangle, n):
                def add_rgba(triangle, colour, opacity):
                    return np.array([
                        [*triangle[0][:3], *colour, opacity, *triangle[0][7:]],
                        [*triangle[1][:3], *colour, opacity, *triangle[1][7:]],
                        [*triangle[2][:3], *colour, opacity, *triangle[2][7:]],
                    ])
                if n==0:
                    return add_rgba(triangle, (np.random.random(),)*3, 1)
                
                new = []

                bl, t, br = triangle

                mid_l, mid_r, mid_b = (bl+t)/2, (t+br)/2, (br+bl)/2,

                new.extend(make_n_subdivisions(np.array([bl, mid_l, mid_b]), n-1)) # bl
                new.extend(make_n_subdivisions(np.array([mid_l, t, mid_r]), n-1)) # t
                new.extend(make_n_subdivisions(np.array([mid_b, mid_r, br]), n-1)) # br
                new.extend(make_n_subdivisions(np.array([mid_l, mid_r, mid_b]), n-1)) # c

                return new
            
            iterated = []

            for triangle in two_triangles:
                iterated.extend(make_n_subdivisions(triangle, n_subdivisions))

            return iterated




        self.back_wall = np.array(iterate_square([np.array([
            [-10, 10,  10, 0.75, 0.15, 0.15, 1, 0, -1, 0],
            [ 10, 10,  10, 0.75, 0.15, 0.15, 1, 0, -1, 0],
            [ 10, 10, -10, 0.75, 0.15, 0.15, 1, 0, -1, 0]]), np.array([
            [ 10, 10, -10, 0.75, 0.15, 0.15, 1, 0, -1, 0],
            [-10, 10, -10, 0.75, 0.15, 0.15, 1, 0, -1, 0],
            [-10, 10,  10, 0.75, 0.15, 0.15, 1, 0, -1, 0]])],
            n_subdivisions=6), dtype=np.float32)
        self.back_wall_vao = create_vao(self.back_wall, store_normals=True)


        self.origin = np.array([0, 0, 0, 0, 0, 0, 1],dtype=np.float32)
        self.origin_vao = create_vao(self.origin)



        self.octasphere = RoundedOctahedron()


        l = 15
        self.xyz = np.array([
            [0, 0, 0, 1, 0, 0, 1],
            [l, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1],
            [0, l, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 0, l, 0, 0, 1, 1],
        ]).astype(np.float32)
        self.xyz_vao = create_vao(self.xyz)


        self.light_source = np.array([*shaders.light_source_pos, *shaders.light_source_colour, 1],
                                     dtype=np.float32)
        self.light_source_vao, self.light_source_vbo = create_vao(self.light_source, return_vbo=True)




    def on_render(self, shaders):

        glUseProgram(shaders.object_shader_program)
        shaders.set_uniforms(shaders.object_shader_program)

        draw_vao(self.origin_vao, GL_POINTS, 1)
        draw_vao(self.octasphere.vao, GL_TRIANGLES, self.octasphere.data.shape[0])
        draw_vao(self.back_wall_vao, GL_TRIANGLES, self.back_wall.shape[0])
        #draw_vao(self.xyz_vao, GL_LINES, self.xyz.shape[0])


        #if not shaders.paused:
        #    mult = 0.01
        #    shaders.light_source_pos += np.array([0, 0, np.random.random()*mult], dtype=np.float32)
        #    self.light_source[:3]    += np.array([0, 0, np.random.random()*mult], dtype=np.float32)
        #    update_vbo(self.light_source_vbo, self.light_source)


        glUseProgram(shaders.lighting_shader_program)
        shaders.set_uniforms(shaders.lighting_shader_program)
        draw_vao(self.light_source_vao, GL_POINTS, self.light_source.shape[0], gl_point_size=25)


class Item(Matrices):
    def __init__(self):
        super().__init__()

        self.position = np.array([0, 0, 0, 1])

    def translate(self, x, y, z):
        self.position = super().translate(x, y, z) @ self.position
    
    def rotate(self, r):
        self.position = super().rotate(r) @ self.position
        
    def rotate_around_p(self, p, r,):
        mk = super().rotate_around_p(p, r)
        self.position = mk @ self.position




class RoundedOctahedron(Item):
    def __init__(self):
        super().__init__()

        self.build_octasphere()

    def make_octahedron_triangles(self, vert_dist, centre=np.array([0, 0, 0])):
        cx, cy, cz = centre

        back   = np.array([          cx, cy,           cz-vert_dist])
        front  = np.array([          cx, cy,           cz+vert_dist])
        left   = np.array([cx-vert_dist, cy,                     cz])
        right  = np.array([cx+vert_dist, cy,                     cz])
        top    = np.array([          cx, cy+vert_dist,           cz])
        bottom = np.array([          cx, cy-vert_dist,           cz])

        t1 = np.array([back, right, top])
        t2 = np.array([front, right, top])
        t3 = np.array([front, left, top])
        t4 = np.array([back, left, top])
        t5 = np.array([back, right, bottom])
        t6 = np.array([front, right, bottom])
        t7 = np.array([front, left, bottom])
        t8 = np.array([back, left, bottom])

        return np.array([t1, t2, t3, t4, t5, t6, t7, t8])
    
    def make_n_subdivisions(self, triangle, n):
        if n==0:
            return self.add_rgba(triangle, (np.random.random(),)*3, 1)

        new = []

        bl, t, br = triangle

        mid_l, mid_r, mid_b = (bl+t)/2, (t+br)/2, (br+bl)/2,

        new.extend(self.make_n_subdivisions(np.array([bl, mid_l, mid_b]), n-1)) # bl
        new.extend(self.make_n_subdivisions(np.array([mid_l, t, mid_r]), n-1)) # t
        new.extend(self.make_n_subdivisions(np.array([mid_b, mid_r, br]), n-1)) # br
        new.extend(self.make_n_subdivisions(np.array([mid_l, mid_r, mid_b]), n-1)) # c

        return new

    def add_rgba(self, triangle, colour, opacity):
        return np.array([
            [*triangle[0], *colour, opacity],
            [*triangle[1], *colour, opacity],
            [*triangle[2], *colour, opacity],
        ])


    def round_triangle(self, triangle, lngth, centre=np.array([0, 0, 0])):
        points = triangle[:, :3]
        colours = triangle[:, 3:]


        dist = points - centre
        norms = np.linalg.norm(dist, axis=1)
        vectors = dist / norms[:, np.newaxis]
        arms = vectors * lngth


        rounded = np.empty((triangle.shape[0], 10), dtype=np.float32)
        rounded[:, :3] = arms
        rounded[:, 3:7] = colours
        rounded[:, 7:] = vectors # the normals of every corner is just the distance from
                                    # the centre to it, normalised

        return rounded

    def build_octasphere(self, vert_dist = 5, n_subdivisions=5):
        num_points = 8 * 3 * 4**n_subdivisions
        self.altered_octahedron = np.empty((num_points, 10), dtype=np.float32)
        octahedron_triangles = self.make_octahedron_triangles(vert_dist) # returns shape (n, 3)


        for i, triangle in enumerate(octahedron_triangles):
            triangle_subdivided = self.make_n_subdivisions(triangle, n_subdivisions) # returns shape (n, 7)
            rounded_triangle = self.round_triangle(np.array(triangle_subdivided), vert_dist) # returns shape (n, 10)

            self.altered_octahedron[(i) * num_points//8 : (i+1) * num_points//8, :] = rounded_triangle

        self.data = self.altered_octahedron
        self.vao, self.vbo = create_vao(self.data, store_normals=True, return_vbo=True)