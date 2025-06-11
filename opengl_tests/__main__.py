from opengl_tests._1_my_the_force_awakens.window import *
from opengl_tests._2_rotation_circulation.window import *
from opengl_tests._3_binary_system.window import *
from opengl_tests._4_opacity_triangles.basic_window import *
from opengl_tests._5_inside_objects.basic_window import *
from opengl_tests._6_joule_collisions.basic_window import *
from opengl_tests._7_true_base_for_copying.window import *
from opengl_tests._8_points.basic_window import *
from opengl_tests._9_particle_life.basic_window import *
from opengl_tests._10_shaders.basic_window import *
from opengl_tests._11_clicking_lighting.window import MoreShadersOpenGL


if __name__ == "__main__":
    app = MoreShadersOpenGL() # _11_
    #app = UsesShaders() # _10_
    #app = ParticleLife() # _9_
    #app = PointsStuff() # _8_
    #app = Window() # _7_
    #app = CollisionFunctions() # _6_
    #app = window_stuff() # _5_
    #app = OpacityTriangles() # _4_
    #app = BinarySystem() # _3_
    #app = rotation_circulation_of_sphere_test() # _2_
    #app =  MyForceAwakens() # _1_
    app.main()