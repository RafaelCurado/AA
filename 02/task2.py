# Divide-and-conquer task

a = 2

def f(b):
    if (b==0):
        return 1
    return f(b/2)*f((b+1)/2)


print(f(2))