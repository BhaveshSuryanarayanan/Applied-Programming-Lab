def isbn10_validator(s):

    s = s.replace('-','')
    for i in range(len(s)):
        if not s[i].isnumeric() and not (i==len(s)-1 and s[i]=='X'):
            return None
    
    if len(s)==9:
        # print(s,len(s))
        ans = str(calcisbn(s)%11)
        # print(ans)
        if ans=='10':
            return 'X'
        else:
            return ans
    
    elif len(s)==10:
        # print(calcisbn(s))
        return (calcisbn(s)%11==0)
    
    else:
        return None

def calcisbn(s):
    ans = 0
    for i in range(len(s)):
        if s[i]=='X':
            ans+=10*(i+1)
        else:
            ans += int(s[i])*(i+1)
    # print(ans)
    return ans

	
	
	
isbn="007462542"

print(isbn10_validator(isbn))