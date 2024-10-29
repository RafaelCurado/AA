def d(i,j):
    if (i == 0 or j == 0):
        return 1
    return d(i-1,j) + d(i-1,j-1) + d(i,j-1)




print(d(11,11))