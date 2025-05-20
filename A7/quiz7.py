def subsetsum(L, S):
    n = len(L)
    for i in range(n):
        for j in range(i,n):
            if sum(L[i:j+1])==S:
                return (i,j+1)
    return (-1,-1)
    	
r = subsetsum([1, 2, 3], 6)
print(r)