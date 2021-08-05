def naturalsum_lim(limit):
    """Suma números naturales consecutivos hasta un tope.

    """
    sum = 0
    i = 0
    while sum + i <= limit:
        sum += i
        i += 1
    return sum

print(naturalsum_lim(9))

# La palabra clave assert recibe una expresión verdadera o falsa, y falla si es falsa. 
# Si es verdadera no hace nada, con lo cual es perfecto para hacer comprobaciones 
# a mitad del código que no estorben mucho.

assert naturalsum_lim(11) == 1 + 2 + 3 + 4