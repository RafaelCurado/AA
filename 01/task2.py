def r1(n):
    if(n == 0): 
        return 0
    return 1 + r1(n-1)


def r2(n):
    if (n == 0):
        return 0
    if (n == 1):
        return 1
    return n + r2(n-2)


def r3(n):
    if (n == 0): 
        return 0
    return 1 + 2*r3(n-1)


def r4(n):
    if (n == 0):
        return 0
    return 1 + r4(n-1) + r4(n-1)




def main():
    a = r2(55)
    print(a)



main()