import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def check_keys(window):
    break_loop = False
    state = glfw.get_key(window, glfw.KEY_ESCAPE)
    if state == glfw.PRESS:
        glfw.terminate()
        break_loop = True
    
    return break_loop