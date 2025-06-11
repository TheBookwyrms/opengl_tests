from OpenGL.GL import *

def create_vao(
        data,
        n_per_vertice = 3,
        n_per_colour  = 3,
        n_per_opacity  = 1,
        n_per_normal  = 3,
        return_vbo    = False,
        store_normals = False,
        ):

    len_ptr = n_per_vertice + n_per_colour + n_per_opacity + (n_per_normal if store_normals else 0)
    stride = len_ptr * data.itemsize

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, n_per_vertice, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    c_offset = n_per_vertice * data.itemsize
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, n_per_colour, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(c_offset))

    o_offset = (n_per_vertice + n_per_colour) * data.itemsize
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, n_per_opacity, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(o_offset))

    if store_normals:
        n_offset = (n_per_vertice + n_per_colour + n_per_opacity) * data.itemsize
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, n_per_normal, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(n_offset))

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    if return_vbo:
        return vao, vbo

    return vao


def update_vbo(vbo, data):
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


def draw_vao(vao, draw_type, n, gl_point_size=10):
    glBindVertexArray(vao)
    glPointSize(gl_point_size)
    glDrawArrays(draw_type, 0, n)
    glBindVertexArray(0)