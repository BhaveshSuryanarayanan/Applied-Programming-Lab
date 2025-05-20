import numpy as np
from math import *
import time

def mul2by2(a,b):
    m1 = (a[0][0]+a[1][1])*(b[0][0]+b[1][1])
    m2 = (a[1][0]+a[1][1])*b[0][0]
    m3 = a[0][0]*(b[0][1]-b[1][1])
    m4 = a[1][1]*(b[1][0]-b[0][0])
    m5 = (a[0][0]+a[0][1])*b[1][1]
    m6 = (a[1][0]-a[0][0])*(b[0][0]+b[0][1])
    m7 = (a[0][1]-a[1][1])*(b[1][0]+b[1][1])
    
    c = [[m1+m4-m5+m7, m3+m5], [m2+m4, m1-m2+m3+m6]]
    
    return c

def least_powerof2(n):
    if(n==1):
        return 1
    p = ceil(log(n,2))
    if int(pow(2,p-1)) == n:
        return n
    
    else:
        return int(pow(2,p))
    
    
def convert(a):
    n, m = a.shape
    N = least_powerof2(n)
    M = least_powerof2(m)
    
    # Create a new array of zeros with the desired shape
    padded_array = np.zeros((N, M), dtype=a.dtype)
    
    # Copy the original array into the top-left corner of the new array
    padded_array[:n, :m] = a
    
    return padded_array
    
def split(x):
    row, col = x.shape
    r, c = row//2, col//2
    return x[:r,:c], x[:r,c:], x[r:,:c], x[r:,c:]


def strassen(x,y):
    if len(x)==1:
        return x*y
    
    a,b,c,d = split(x)
    e,f,g,h = split(y)
    
    p1 = strassen(a,f-h)
    p2 = strassen(a+b,h)
    p3 = strassen(c+d,e)
    p4 = strassen(d,g-e)
    p5 = strassen(a+d,e+h)
    p6 = strassen(b-d,g+h)
    p7 = strassen(a-c,e+f)
    
    c11 = p5 + p4 - p2 + p6
    c12 = p1 + p2
    c21 = p3 + p4
    c22 = p1 + p5 - p3 - p7
    c = np.vstack((np.hstack((c11,c12)),np.hstack((c21,c22))))
    
    return c

def matrix_multiply(A,B): 
    m,n = A.shape
    n,k = B.shape
    A = convert(A)
    B = convert(B)
    C = strassen(A,B)
    return C[:m,:k]
    
    
    
    
    
# A = [[1,0,1,0],[0,1,1,0],[1,0,1,0],[0,1,1,0]]
# B = [[1,0,1,0],[0,1,1,0],[1,0,1,0],[0,1,1,0]]
# A = [[1,0],[0,1]]
# B = [[1,2],[3,4]]

# A = [[1,0,0],[0,2,0],[0,0,2]]
# B = [[2,0,0],[0,3,0],[0,0,2]]  

# # # for i in range(1,10):
# # #     print(i,least_powerof2(i))
# A = np.array(A)
# B = np.array(B)
# print(matrix_multiply(A,B))

m,n,k= 100,100,100
a = np.random.randint(0, 101, size=(m, n))
b = np.random.randint(0, 101, size=(n, k))

t1 = time.time()
c = matrix_multiply(a,b)
t2 = time.time()
print(t2-t1)
# print(c)