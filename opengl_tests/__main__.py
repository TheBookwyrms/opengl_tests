from opengl_tests._6_joule_collisions.basic_window import *
from opengl_tests._5_inside_objects.basic_window import *
from opengl_tests._4_opacity_triangles.basic_window import *
from opengl_tests._3_solar_system.window import *
from opengl_tests._2_rotation_circulation.window import *
from opengl_tests._1_my_the_force_awakens.window import *

if __name__ == "__main__":
    app = CollisionFunctions() # _6_
    #app = window_stuff() # _5_
    #app = OpacityTriangles() # _4_
    #app = SolarSystem() # _3_
    #app = rotation_circulation_of_sphere_test() # _2_
    #app =  MyForceAwakens() # _1_
    app.main()