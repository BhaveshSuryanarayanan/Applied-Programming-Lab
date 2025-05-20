def swap_row(a,i,j):
    a[i],a[j] = a[j],a[i]
    

def gausselim(A,B):
    a=A
    for i in range(len(a)):
        a[i].append(B[i])
    # n,m =a.shape
    n = len(a)
    m = len(a[0])
    # print(a,n,m)
    if m-1<n:
       return -1
    
    n = min(n,m-1)
    for i in range(n):
        # print(a)
        i_max = i
        max_pivot = a[i][i]
        for k in range(i+1,n):
            if(max_pivot<abs(a[k][i])):
                max_pivot = abs(a[k][i])
                i_max = k   
                     
        # if not a[i_max][i]:
        #     return -1
        
            
        if(i_max!=i):
            swap_row(a,i,i_max)
        # print(a,i)
            
        for k in range(n):
            if(k==i):
                continue
            ratio = a[k][i]/a[i][i]
            # print(ratio)
            for j in range(i+1,m):
                a[k][j] -= (a[k][i]/a[i][i])*a[i][j]
            a[k][i]=0
                
        # print(a,i)
    
    sol = []
    for i in range(n):
        sol.append(a[i][m-1]/a[i][i])
    return sol

a = [[1,2,3,6],[0,0,1,0],[3,5,1,9]]
A = [row[:-1] for row in a]
B = [row[-1] for row in a]
	
A = [ [2,3], [1,-1] ]
B = [6,1/2]
# print(A,B)
sol = gausselim(A,B)
print(sol)