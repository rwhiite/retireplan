def fixedInvestor(principal, rate, years, contribution):
    balance = principal
    history = []
    for _ in range(years):
        balance = balance * (1 + rate) + contribution
        history.append(balance)
    return balance, history


def variableInvestor(principal, rateList, contribution):
    balance = principal
    history = []
    for r in rateList:
        balance = balance * (1 + r) + contribution
        history.append(balance)
    return balance, history


def finallyRetired(principal, withdrawal, rate, years=None):
    """
    Simulate withdrawals post-retirement.
    If years is None, run until balance reaches zero.
    If years is specified, simulate exactly that many years.
    """
    balance = principal
    year = 0
    history = []

    if years is None:  # old behavior: until depletion
        while balance > 0:
            balance = balance * (1 + rate) - withdrawal
            if balance < 0:
                balance = 0
            history.append(balance)
            year += 1
    else:
        for _ in range(years):
            balance = balance * (1 + rate) - withdrawal
            if balance < 0:
                balance = 0
            history.append(balance)
            year += 1

    return year, history


def maximumExpensed(principal, rate, years):
    """
    Binary search to find maximum sustainable annual withdrawal
    over exactly 'years' retirement years.
    """
    low, high = 0, principal
    for _ in range(100):
        mid = (low + high) / 2
        b = principal
        for _ in range(years):
            b = b * (1 + rate) - mid
            if b < 0:
                break
        if b > 0:
            low = mid
        else:
            high = mid
    return low
