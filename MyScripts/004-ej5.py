# Fibonacci using iteration

def fib(n):
    """ Fibonacci sequence:
        f_n  = f_(n-1) + f_(n-2); with f_0 = 0, f_1 = 1
        Uses iteration to solve
    """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

print(fib(0), fib(3), fib(10))

# Fibonacci using recursive methods

def fib_recursive(n):
    """ Fibonacci sequence:
        f_n  = f_(n-1) + f_(n-2); with f_0 = 0, f_1 = 1
        Uses recusive methods to solve
    """
    if n == 0:
        res = 0
    elif n == 1:
        res = 1
    else:
        res = fib_recursive(n - 1) + fib_recursive(n - 2)
    return res

print(fib_recursive(0), fib_recursive(3), fib_recursive(10))

# Print a list of the n first numbers

def n_first(n):
    F = fib_recursive
    listt = []
    for i in range(n):
        listt.append(F(i))
    return listt

print(n_first(10))
