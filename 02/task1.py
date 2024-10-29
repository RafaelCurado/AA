# Brute-force task

a = 2
count = 0

def f(b):
    global count
    if (b==0):
        return 1
    elif (b==1):
        return a
    count+=1
    return a*f(b-1)


print("result: "+str(f(7)))
print("mult count: "+str(count))

