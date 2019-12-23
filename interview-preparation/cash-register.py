# 33 cents = 1 quarter (25), 1 dime 10, 1 nickel(5), 3 pennies(1)
# num_count(31)


def num_coin(cents):
    if cents < 0:
        return 0
    coins = [25, 10, 5, 1]
    num_of_coins = 0
    for coin in coins:
        num_of_coins += cents // coin
        cents = cents % coin
        if cents == 0:
            break
    return num_of_coins
        
cents = 532
print(num_coin(cents))

def num_coins(cents):
    if cents < 0:
        return 0
    coins = [25, 10, 5, 1]
    count= 0
    for coin in coins:
        if coin >= cents:
            count += cents // coin
            cent = cent % coin
            if cents == 0:
                break
        continue
    return count

cents = 2
print(num_coins(cents))

    
