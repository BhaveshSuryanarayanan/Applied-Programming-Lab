import numpy as np

def is_matrix(a):
    if len(a) == 0:
        raise ValueError("Invalid Matrix Dimensions")

    for row in a:
        if not isinstance(row,list):
            raise TypeError("Input should be a 2D matrix")

        if len(row)==0 or len(row) != len(a[0]):
            raise ValueError("Invalid Matrix Dimensions")

        for element in row:
            if not (isinstance(element, int) or isinstance(element,float) or isinstance(element,complex)):
                raise TypeError("Matrix has invalid datatypes")

    return True


def check_inputs(a, b):
    is_matrix(a)
    is_matrix(b)

    if len(a[0]) != len(b):
        raise ValueError("Matrices have incompatible dimensions")


def matrix_multiply(a, b):
    check_inputs(a, b)
    m = len(a)
    n = len(a[0])
    k = len(b[0])

    c = [[0 for _ in range(k)] for _ in range(m)]
    # print(c)
    for i in range(m):
        for j in range(k):
            c[i][j] = sum(a[i][p] * b[p][j] for p in range(n))
    return c


def print_matrix(a):
    for row in a:
        print(row)


# A = [[1,0,0],[0,2,0],[0,0,2]]
# B = [[2,0,0],[0,3,0],[0,0,2]]
# A = np.array(A)
# B = np.array(B)


# m,n,k=500,100,100
# a = np.random.randint(0, 101, size=(m, n))
# b = np.random.randint(0, 101, size=(n, k))

# import time
# t1 = time.time()
# c = matrix_multipliy(a,b)
# t2 = time.time()
# print(t2-t1)

# a = [1]
# b = [1]
# c = matrix_multiply(a, b)
# print(c)
