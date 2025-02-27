import numpy as np


class a:
    def __init__(self):
        pass


l = []
for i in range(15):
    p = a()
    l.append(p)


grid = np.empty((3, 2), dtype=a)
print(grid)
grid[0, 0] = (l[0], l[1], l[2])
grid[0, 1] = (l[3], l[4])
print(grid)

print(type([2]))