import numpy as np

a = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
b = np.array([1, 4, 7])
#print(np.matmul(a, b))


class a:
    def __init__(self):
        self.test = 1

class b(a):
    def __init__(self):
        super().__init__()

one=a()
two=b()
print(one.test, two.test)