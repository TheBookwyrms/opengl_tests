import numpy as np


t1 = np.eye(4)

t2 = np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1],
])

print(t1@t2)
print()
print(t2@t1)


a = 15
f0 = 0/1
f1 = 1/2
f2 = 3/4
f3 = 1/1

print(a*f0//1)
print(a*f1//1)
print(a*f2//1)
print(a*f3//1)