def find_maxima(x):
    """Halla los índices de los máximos relativos"""
    idx = []
    N = len(x)
    if x[1] < x[0]:
        idx.append(0)
    for i in range(1, N - 1):
        if x[i-1] < x[i] and x[i+1] < x[i]:
            idx.append(i)
    if x[-2] < x[-1]:
        idx.append(N - 1)
    return idx


#___ Test ___#
def test1():
    lista = [1, 2, 1]
    resultado_esperado = [1]
    resultado = find_maxima(lista)
    assert resultado == resultado_esperado


def test2():
    lista = [1, 2, 3, 2, 1]
    resultado_esperado = [2]
    resultado = find_maxima(lista)
    assert resultado == resultado_esperado


def test3():
    lista = [1, 2, 3]
    resultado_esperado = [2]
    resultado = find_maxima(lista)
    assert resultado == resultado_esperado


test1()
test2()
test3()
