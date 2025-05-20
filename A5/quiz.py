def palin(n):
    s = [int(x) for x in str(n)]
    
    # First check if already palindrome - then inc by 1
    lmid = (len(s)-1) // 2 
    mid  = (len(s) + 1) // 2 - 1
    p = True
    for i in range(lmid+1):
        if s[i] != s[-i-1]:
            p = False
            break
    if p:
        s = [int(x) for x in str(n+1)]
        
    for i in range(lmid+1):
        s[-i-1] = s[i]
    m = int(''.join([str(x) for x in s]))
    # print('//',m)
    if m>n:
        return m
    else:
        i = lmid
        while True and i>=0:
            if s[i]==9:
                s[i]=0
                s[-i-1]=0
                i-=1
            else:
                s[i]+=1
                s[-i-1] = s[i]
                break

    return int(''.join([str(x) for x in s]))


print(palin(1))
print(palin(9))
print(palin(11))
print(palin(999))
print(palin(1001))