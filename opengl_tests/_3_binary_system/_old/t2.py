import numpy as np

a = np.array([
    [1, 2, 3, 1, 1, 1],
    [4, 5, 6, 1, 1, 1],
    [7, 8, 9, 1, 1, 1]
])
b = np.array([1, 4, 7])
a[:, :3]-=b
print(a)

'''
p.data = np.array((
    [x, y, z, c, c, c],
    [x, y, z, c, c, c],
    ...
    [x, y, z, c, c, c],
    [x, y, z, c, c, c],
))
'''

'''
p.data[:, :3] = np.matmul((p.data[:, :3] - p.prev_s), (p.rot_mat)) + p.curr_s

'''




class a:
    def __init__(self):
        self.test = 1

class b(a):
    def __init__(self):
        super().__init__()

one=a()
two=b()
#print(one.test, two.test)