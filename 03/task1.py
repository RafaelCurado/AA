from functools import cache

@cache
def f(n):
    if(n==0):
        return 0
    if(n==1):
        return 1
    return f(n-1)+f(n-2)



# for n in range(0,21):
#     print("f("+str(n)+"): "+str(f(n)))


print(f(40))