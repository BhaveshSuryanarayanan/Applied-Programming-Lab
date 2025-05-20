from collections import defaultdict

def dedup(l):
    freq = defaultdict(bool)
    ans = []
    
    for el in l:
        if not freq[el]:
            ans.append(el)
            freq[el] = True
    return ans

l = [4, 2, 9, 4, 7, 2, 5]
e = [4, 2, 9, 7, 5]
r = dedup(l)
print(r)
if (r == e):
  print("PASS")
else:
  print("FAIL")