import glfw
from glfw.GLFW import *
import time
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import imgui
from imgui.integrations.glfw import GlfwRenderer




def main():
    if not glfw.init():
        return
    width, height = 500, 500
    window = glfw.create_window(width, height, "test", None, None)
    glfw.make_context_current(window)

    glfw.get_framebuffer_size(window)

    imgui.new_frame()
    imgui.begin("testing")
    imgui.text("test test")
    imgui.end()

    start = time.time()

    while not glfw.window_should_close(window):


        state = glfw.get_key(window, glfw.KEY_ESCAPE)
        if state == glfw.PRESS:
            glfw.terminate()
            break

        #gluSphere(GLUquadric(),10,10,10)
        glfw.swap_buffers(window)
        glfw.poll_events()

    print("loop broken")

if __name__ == "__main__":
    main()