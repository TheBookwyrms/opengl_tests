import numpy as np

a = np.array([2, 8, 15])
b = np.array([1, 5, 23])
'''
goal:
(23-15)**2 + (5-8)**2 + (1-2)**2
64 + 9 + 1
74
'''

c = (b-a)**2
print(c)