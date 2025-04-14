import numpy as np

from opengl_tests._11_HEP_display_1.vbo_vao_stuff import *
#from opengl_tests._11_HEP_display_1_algorithm.detection import *

class DetectionHulls:
    def __init__(self):
        pass

    def make_points_from_xyz(self, low_x, high_x, low_y, high_y, low_z, high_z, colour, opacity):
        p1 = np.array([low_x,  low_y,  low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    0)    # BFL
        p2 = np.array([high_x, low_y,  low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    0)    # BFR
        p3 = np.array([low_x,  high_y, low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, 0)    # BBL
        p4 = np.array([high_x, high_y, low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, 0)    # BBR
        p5 = np.array([low_x,  low_y,  high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    zlen) # TFL
        p6 = np.array([high_x, low_y,  high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    zlen) # TFR
        p7 = np.array([low_x,  high_y, high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, zlen) # TBL
        p8 = np.array([high_x, high_y, high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, zlen) # TBR

        return p1, p2, p3, p4, p5, p6, p7, p8
    
    def vec3_to_vec7(self, p, colour, opacity):
        return np.array([p[0], p[1], p[2], colour[0], colour[1], colour[2], opacity])

    def make_prism_triangles(self, p1, p2, p3, p4, p5, p6, p7, p8):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        # front face
        tf1 = [p1, p2, p5]
        tf2 = [p2, p5, p6]

        # back face
        tb1 = [p3, p4, p7]
        tb2 = [p4, p7, p8]
        
        # left face
        tl1 = [p1, p3, p5]
        tl2 = [p3, p5, p7]

        # right face
        tr1 = [p2, p4, p6]
        tr2 = [p4, p6, p8]

        # bottom face
        tB1 = [p1, p2, p3]
        tB2 = [p2, p3, p4]

        # top face
        tT1 = [p5, p6, p7]
        tT2 = [p6, p7, p8]
        
        
        all_t = []

        all_t.extend(tf1)
        all_t.extend(tf2)
        all_t.extend(tb1)
        all_t.extend(tb2)
        all_t.extend(tl1)
        all_t.extend(tl2)
        all_t.extend(tr1)
        all_t.extend(tr2)
        #all_t.extend(tB1) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tB2) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tT1) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tT2) # hiding these 4 faces allows for seeing through convex hull

        return all_t
    
    def scale_points(self, hull_bounds, fan_out, scale_factor=2):
        '''
        hull_bounds = [1, 2, 3, 4, 5, 6, 7, 8]
        fan_out = [(1, 8), (2, 7), (3, 6), (4, 5)]
        '''

        vec = lambda p1, p2 : p1-p2

        line_vectors = []
        for line in fan_out:
            vec_p1_p2 = vec(line[0], line[1])
            unit_vec = vec_p1_p2/np.linalg.norm(vec_p1_p2)
            line_vectors.append(5*unit_vec) # vec from p0 to p1

        
        scaled_p0 = line_vectors[0]+hull_bounds[0]
        scaled_p1 = line_vectors[1]+hull_bounds[1]
        scaled_p2 = line_vectors[2]+hull_bounds[2]
        scaled_p3 = line_vectors[3]+hull_bounds[3]
        scaled_p4 = -line_vectors[3]+hull_bounds[4]
        scaled_p5 = -line_vectors[2]+hull_bounds[5]
        scaled_p6 = -line_vectors[1]+hull_bounds[6]
        scaled_p7 = -line_vectors[0]+hull_bounds[7]

        #print(hull_bounds[0], line_vectors[0], scaled_p0)
        #print(hull_bounds[7], line_vectors[0], scaled_p7)
        #print()

        scaled_hull_bounds = [scaled_p0, scaled_p1,
                              scaled_p2, scaled_p3,
                              scaled_p4, scaled_p5,
                              scaled_p6, scaled_p7]
        
        scaled_fan_out = [
            (scaled_p0, scaled_p7),
            (scaled_p1, scaled_p6),
            (scaled_p2, scaled_p5),
            (scaled_p3, scaled_p4),
        ]


        return scaled_hull_bounds, scaled_fan_out


    def get_hull_returns(self):
        # hull_bounds, fan_out = "do some stuff"

        '''
        hull_bounds = [1, 2, 3, 4, 5, 6, 7, 8]
        == [TFL, TBL, TFR, TBR, BFL, BBL, BFR, BBR]

        fan_out = [(1, 8), (2, 7), (3, 6), (4, 5)]
        '''

        

        #scintillators = [
        #    [
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (1,1),
        #        (0,1),
        #        (1,1),
        #    ],
        #    [
        #        (0,1),
        #        (1,0),
        #        (0,0),
        #        (0,1),
        #        (1,1),
        #        (1,0),
        #    ],
        #]
        #
        #a = scintillators_to_bounds(scintillators)
        #print(a)

        #scintillators = [
        #    [
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #    ],
        #    [
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #        (0,1),
        #    ],
        #]
        #hull_bounds, fan_out = scintillators_to_bounds(scintillators)


        # # TEST DATA
        # p1, p2, p3, p4 = (1, 3,   7), (1, 4,   7), (3, 3,   7), (3, 4,   7)
        # p5, p6, p7, p8 = (1, 3, -14), (1, 4, -14), (3, 3, -14), (3, 4, -14)
        p1, p2, p3, p4 = (5, 3, 7), (5, 5, 7), (7, 3, 7), (7, 5, 7)
        p5, p6, p7, p8 = (5, 3, 4), (5, 5, 4), (7, 3, 4), (7, 5, 4)
        hull_bounds =[p1, p2, p3, p4, p5, p6, p7, p8]
        fan_out = [(p1, p8), (p2, p7), (p3, p6), (p4, p5)]



        return np.array(hull_bounds).astype(np.float32), np.array(fan_out).astype(np.float32)

    def create_hull_data(self):
        '''

        works with actual values of structure

        given:
        8 vertices bounding prism
            - coordinates on most extreme level
        sorted

        data cleaning:
        - convert coordinate systems
            - convert x, y, z, point values into local values
        - determine point order
        
        3 steps:
        - make inside prism
        - make upwards fan
        - make downwards fan

        '''

        hull_bounds, fan_out = self.get_hull_returns()
        '''
        hull_bounds = [1, 2, 3, 4, 5, 6, 7, 8]
        == [TFL, TBL, TFR, TBR, BFL, BBL, BFR, BBR]

        fan_out = [(1, 8), (2, 7), (3, 6), (4, 5)]
        '''

        hull_colour = [0.5, 0, 0.5]
        hull_opacity = 0.8

        p1, p2, p3, p4, p5, p6, p7, p8 = self.make_points_from_xyz(
                low_x   = hull_bounds[0][0],
                high_x  = hull_bounds[3][0],
                low_y   = hull_bounds[4][1],
                high_y  = hull_bounds[3][1],
                low_z   = hull_bounds[4][2],
                high_z  = hull_bounds[3][2],
                colour  = hull_colour,
                opacity = hull_opacity,
            )
        hull_prism_triangles = self.make_prism_triangles(
            p1, p2, p3, p4, p5, p6, p7, p8
        )

        scaled_hull_bounds, scaled_fan_out = self.scale_points(hull_bounds, fan_out, scale_factor=2)
        
        top_triangle_fans = self.make_prism_triangles(
            p1 = self.vec3_to_vec7(       hull_bounds[0], hull_colour, hull_opacity),
            p2 = self.vec3_to_vec7(       hull_bounds[2], hull_colour, hull_opacity),
            p3 = self.vec3_to_vec7(       hull_bounds[1], hull_colour, hull_opacity),
            p4 = self.vec3_to_vec7(       hull_bounds[3], hull_colour, hull_opacity),
            p5 = self.vec3_to_vec7(scaled_hull_bounds[0], hull_colour, hull_opacity),
            p6 = self.vec3_to_vec7(scaled_hull_bounds[2], hull_colour, hull_opacity),
            p7 = self.vec3_to_vec7(scaled_hull_bounds[1], hull_colour, hull_opacity),
            p8 = self.vec3_to_vec7(scaled_hull_bounds[3], hull_colour, hull_opacity),
        )

        bottom_triangle_fans = self.make_prism_triangles(
            p1 = self.vec3_to_vec7(scaled_hull_bounds[4], hull_colour, hull_opacity),
            p2 = self.vec3_to_vec7(scaled_hull_bounds[6], hull_colour, hull_opacity),
            p3 = self.vec3_to_vec7(scaled_hull_bounds[5], hull_colour, hull_opacity),
            p4 = self.vec3_to_vec7(scaled_hull_bounds[7], hull_colour, hull_opacity),
            p5 = self.vec3_to_vec7(       hull_bounds[4], hull_colour, hull_opacity),
            p6 = self.vec3_to_vec7(       hull_bounds[6], hull_colour, hull_opacity),
            p7 = self.vec3_to_vec7(       hull_bounds[5], hull_colour, hull_opacity),
            p8 = self.vec3_to_vec7(       hull_bounds[7], hull_colour, hull_opacity),
        )

        hull_data = []
        hull_data.extend(hull_prism_triangles)
        hull_data.extend(top_triangle_fans)
        hull_data.extend(bottom_triangle_fans)
        self.hull_data = np.array(hull_data).astype(np.float32)


    def create_hull_vao(self):
        self.hull_vao = make_vao_vbo(self.hull_data)[0]
    
    def draw_hull(self):
        draw_vao(self.hull_vao, GL_TRIANGLES, self.hull_data.shape[0])