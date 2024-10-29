# coin row problem

def v1(coins, index=0):
    if index >= len(coins):
        return 0
    pick = coins[index] + v1(coins, index+2)
    skip = v1(coins, index+1)

    return max(pick, skip)


def v2(coins):
    max = max(coins)
    






coins = [5,1,2,10,6,2]

result = v1(coins)
print(result)


v2 = v2(coins)