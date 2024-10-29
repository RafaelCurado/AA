import sys

def f1(n): 
    r = 0; i = 1
    for i in range(n):
        r += 1
    return r


def f2(n):
    r = 0 
    for i in range(n):
        for j in range(n):
            r += 1
    return r

def f3(n):
    r = 0 
    for i in range(n):
        j = i
        for j in range(n):
            r += 1
    return r


def f4(n):
    r = 0 
    for i in range(n):
        for j in range(i):
            r += j
    return r




def main():
    for arg in range(11):
        a = f1(arg)
        print("f1("+str(arg)+"): " + str(a))

        b = f2(arg)
        print("f2("+str(arg)+"): " + str(b))
    
        c = f3(arg)
        print("f3("+str(arg)+"): " + str(c))
        
        d = f4(arg)
        print("f4("+str(arg)+"): " + str(d))

        print("---------------------------------")
        

if __name__ == "__main__":
    sys.exit(main())