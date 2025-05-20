import time
from functools import cache

def timeit(f):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        ans = f(*args, **kwargs)
        t2 = time.time()
        t = (int((t2 - t1) * 1000))
        return ans, t
    return wrapper

@timeit
@cache
def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1)[0] + fib(n-2)[0]  

n = 36
x, t = fib(n)
print(x,t)
