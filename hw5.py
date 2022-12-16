def change(amount, coins):
    """calculate the minimum number of coins required to make up the given amount

    Parameters
    ----------        
    amount: int
        non-negative, the amount of change to be made
    
    coins: list
        coin values

    Returns
    -------
    int
        non-negative integer indicating the minimum number of coins required to make up the given amount
    """
    memo = [0] * (amount + 1)   # use memo to avoid repeated calculation

    def changeHelper(num):  # a helper function
        if num < 0:
            return float("inf")
        if num == 0:
            return 0
        if memo[num - 1] != 0:
            return memo[num - 1]
        res = float("inf")
        for coin in coins:
            res = min(res, changeHelper(num - coin) + 1)
        memo[num - 1] = res
        return memo[num - 1]
    
    return changeHelper(amount)

def giveChange(amount, coins):
    """return the minimum number of coins required to make up the given amount, and the coins in
        that optimal solution

    Parameters
    ----------        
    amount: int
        non-negative, the amount of change to be made
    
    coins: list
        coin values

    Returns
    -------
    [numberOfCoins, listOfCoins]: list
        first member is the minimum number of coins, and second member is a list of the coins in
        that optimal solution
    """
    memo = [[0, []] for _ in range(amount + 1)]   # use memo to avoid repeated calculation

    def giveChangeHelper(num):  # a helper function
        if num < 0:
            return [float("inf"), []]
        if num == 0:
            return [0, []]
        if memo[num - 1][0] != 0:
            return memo[num - 1]
        minNumber = float("inf")
        minList = []
        for coin in coins:
            numberOfCoins, listOfCoins = giveChangeHelper(num - coin)
            if numberOfCoins + 1 < minNumber:
                minNumber = numberOfCoins + 1
                minList = listOfCoins + [coin]
        memo[num - 1] = [minNumber, minList]
        return memo[num - 1]
    
    return giveChangeHelper(amount)
