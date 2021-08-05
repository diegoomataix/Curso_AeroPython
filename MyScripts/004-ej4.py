import numpy as np

def square_root(s):
    """ Function to compute square roots using the Babylonian method
    """
    x = s/2
    while True:
        temp  = x
        x = (1/2) * ( x + (s/x) )
        if temp == x:
            return x
        # Como la convergencia se alcanza rápidamente, llega un momento en que el error 
        # es menor que la precisión de la máquina y el valor no cambia de un paso a otro.

print(square_root(10))

# Check validity using numpy library
check = 10;
print(square_root(check) == np.sqrt(check))
print(square_root(check) - np.sqrt(check))

# Also note these characteristics of the floating point numbers
print(square_root(check) ** 2)
print(np.sqrt(check) ** 2)