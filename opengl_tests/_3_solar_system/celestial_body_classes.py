from opengl_tests._3_solar_system.object_classes.sphere_class import *


class Planet(Sphere):
    def __init__(self,
                 radius=1,
                 x_i=0,
                 y_i=0,
                 z_i=0,
                 x_c=[1,0,0],
                 y_c=[0,1,0],
                 z_c=[0,0,1],
                 center=np.array([0, 0, 0]),
                 vec_maj=np.array([10, 0, 0]),
                 vec_min=np.array([0, 10, 0]),
                 e_c=[1, 1, 1],
                 rot_axis_vec =np.array([4, 9.24345, 0]), # vector equivalent to earth's tilt
                 r_axis_c=np.array([1,1,1]),
                 deg_per_rot=1
                 ):
        super().__init__(radius, x_i, y_i, z_i, x_c, y_c, z_c,
                         center, vec_maj, vec_min, e_c,
                         rot_axis_vec, r_axis_c, deg_per_rot)


class BlackHole(Sphere):
    def __init__(self,
                 radius=1,
                 x_i=0,
                 y_i=0,
                 z_i=0,
                 x_c=[0,0,0],
                 y_c=[0,0,0],
                 z_c=[0,0,0],
                 center=np.array([0, 0, 0]),
                 vec_maj=np.array([10, 0, 0]),
                 vec_min=np.array([0, 10, 0]),
                 e_c=[1, 1, 1],
                 rot_axis_vec =np.array([4, 9.24345, 0]), # vector equivalent to earth's tilt
                 r_axis_c=np.array([1,1,1]),
                 deg_per_rot=1
                 ):
        super().__init__(radius, x_i, y_i, z_i, x_c, y_c, z_c,
                         center, vec_maj, vec_min, e_c,
                         rot_axis_vec, r_axis_c, deg_per_rot)
        
        self.x_i, self.y_i, self.z_i = x_i, y_i, z_i


class Star(Sphere):
    def __init__(self,
                 radius=1,
                 x_i=0,
                 y_i=0,
                 z_i=0,
                 x_c=[0.99,0.44,0],
                 y_c=[0.89,0.55,0],
                 z_c=[0.85,0.72,0],
                 center=np.array([0, 0, 0]),
                 vec_maj=np.array([10, 0, 0]),
                 vec_min=np.array([0, 10, 0]),
                 e_c=[1, 1, 1],
                 rot_axis_vec =np.array([4, 9.24345, 0]), # vector equivalent to earth's tilt
                 r_axis_c=np.array([1,1,1]),
                 deg_per_rot=1
                 ):
        super().__init__(radius, x_i, y_i, z_i, x_c, y_c, z_c,
                         center, vec_maj, vec_min, e_c,
                         rot_axis_vec, r_axis_c, deg_per_rot)
        
        self.x_i, self.y_i, self.z_i = x_i, y_i, z_i