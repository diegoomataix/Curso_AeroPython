def naturalsum(n):
    """Suma los `n` primeros números.

    Ejemplos
    --------
    >>> sumatorio(4)
    10 """
    sum = 0
    for i in range(1, n+1):
        sum +=  i       # same as saying sum = sum + i
    return sum
    
print(naturalsum(4))

# check that the function works using a built in Python function

print(sum(range(1, 4 + 1)))