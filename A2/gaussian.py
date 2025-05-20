import numpy as np

def swap_row(a,i,j):
    a[i],a[j] = a[j],a[i]
    

def gaussian_elimination(a):
    # n,m =a.shape
    n = len(a)
    m = len(a[0])
    if m-1<n:
       return -1
    
    # n = min(n,m-1)
    for i in range(min(n,m-1)):
        i_max = i
        max_pivot = a[i][i]
        for k in range(i+1,n):
            if(max_pivot<abs(a[k][i])):
                max_pivot = abs(a[k][i])
                i_max = k   
                     
        if not a[i_max][i]:
            return -1
        
            
        if(i_max!=i):
            swap_row(a,i,i_max)
        # print(a,i)
            
        for k in range(n):
            if(k==i):
                continue
            ratio = a[k][i]/a[i][i]
            # print(ratio)
            for j in range(i+1,n):
                a[k][j] -= (a[k][i]/a[i][i])*a[i][j]
            a[k][i]=0
                
        # print(a,i)
    
    sol = []
    for i in range(n):
        sol.append(a[i][m-1]/a[i][i])
    return sol

a = [[1,2,3,6],[0,0,1,0],[3,5,1,9]]
# a = np.array(a,dtype=float)
# # swap_row(a,1,0)

# n = 100
# m = n+1
# a = np.random.random((n,m))
sol = gaussian_elimination(a)
print(sol)

# if sol==-1:
#     print("Singular Matrix : no solution")
# else :
#     print(sol)
    
# A = a[:,:-1]
# B = a[:,-1]
# try:
#     x = np.linalg.solve(A,B)
#     print('numpy solution: ' ,x)
#     np.testing.assert_array_almost_equal(sol,x,decimal=6)
#     print('TrUe')
# except:
#     if sol==-1:
#         print('TrUe')
#     else :
#         print('FaLsE')
a = np.array(a)
A = a[:,:-1]
B = a[:,-1]
x = np.linalg.solve(A,B)
print(x)

