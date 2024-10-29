# Decrease-and-conquer task recursive

count = 0
a = 2

def f(b):
    global count
    if (b==0):
        return 1
    if (b==1):
        return a
    
    temp = f(b / 2)
    
    if (b%2==1):
        count += 2
        return a * temp * temp
    if (b%2==0):
        count += 1
        return temp * temp
    

print(f(11))
print(count)