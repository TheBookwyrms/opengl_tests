from opengl_tests._3_solar_system.window import *
from opengl_tests._2_rotation_circulation.window import *
from opengl_tests._1_my_the_force_awakens.window import *

if __name__ == "__main__":
    app = SolarSystem() # _3_
    #app = rotation_circulation_of_sphere_test() # _2_
    #app =  MyForceAwakens() # _1_
    app.main()