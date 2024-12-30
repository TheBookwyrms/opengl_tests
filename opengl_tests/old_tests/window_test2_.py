import glfw
from glfw.GLFW import *
import time
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import imgui
from imgui.integrations.glfw import GlfwRenderer



# initilize imgui context (see documentation)
imgui.create_context()
imgui.get_io().display_size = 100, 100
imgui.get_io().fonts.get_tex_data_as_rgba32()
    



def main():
    if not glfw.init():
        return
    width, height = 500, 500
    window = glfw.create_window(width, height, "test", None, None)
    glfw.make_context_current(window)

    glfw.get_framebuffer_size(window)


    start = time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT)
    
    

        # initilize imgui context (see documentation)
        imgui.create_context()
        imgui.get_io().display_size = 100, 100
        imgui.get_io().fonts.get_tex_data_as_rgba32()

        # start new frame context
        imgui.new_frame()

        # open new window context
        imgui.begin("Your first window!", True)

        # draw text label inside of current window
        imgui.text("Hello world!")

        # close current window context
        imgui.end()

        # pass all drawing comands to the rendering pipeline
        # and close frame context
        imgui.render()
        imgui.end_frame()



        state = glfw.get_key(window, glfw.KEY_ESCAPE)
        if state == glfw.PRESS:
            glfw.terminate()
            break

        #gluSphere(GLUquadric(),10,10,10)
        glfw.swap_buffers(window)


    print("loop broken")

if __name__ == "__main__":
    main()