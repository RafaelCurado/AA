# coin row problem - dynamic programming

def f(coins, n):
    #n = len(coins)
    if (n == 0):
        return 0
    if (n == 1):
        return coins[n]
    
    return max(coins[n] + f(coins,n-2), f(n-1))



coins = [None,5,1,2,10,6,2]
print(f(coins,6))