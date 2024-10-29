import random


trials = 100000
tosses = 3 # number of tosses

h0 = 0
h1 = 0
h2 = 0
h3 = 0

for trial in range(trials):
    
    heads = 0
    tails = 0
    
    for i in range(tosses):
        flip = random.randint(0,1)
        if (flip == 0):
            heads += 1
        else:
            tails += 1

    if (heads == 0):
        h0 += 1
    if (heads == 1):
        h1 += 1
    if (heads == 2):
        h2 += 1
    if (heads == 3):
        h3 += 1


print("0 heads - "+str(h0))
print("1 heads - "+str(h1))
print("2 heads - "+str(h2))
print("3 heads - "+str(h3))



# print("heads:"+str(heads))
# print("tails:"+str(tails))

