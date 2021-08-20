###_________________________________ Numba _________________________________###

# En ocasiones nos encontraremos con algoritmos que no serán fácilmente vectorizables 
# o expresables en operaciones sobre arrays de NumPy, y sufriremos los problemas 
# de rendimiento de Python. En este notebook vamos a hacer un repaso exhaustivo 
# de cómo acelerar sustancialmente nuestro código Python usando numba. Esta clase 
# está basada en el artículo http://pybonacci.org/2015/03/13/como-acelerar-tu-codigo-python-con-numba/

##________ ¿Qué es numba? ________##
# numba es un compilador JIT (just-in-time) de Python que genera código máquina 
# para CPU o GPU utilizando la infraestructura LLVM especializado en aplicaciones 
# numéricas. Vamos a ver un ejemplo muy básico de cómo funciona:
    
import numpy as np
from numba import njit

arr2d = np.arange(20 * 30, dtype=float).reshape(20,30)

np.sum(arr2d) # timing: The slowest run took 10.82 times longer than the fastest. 
              # This could mean that an intermediate result is being cached.
              # 100000 loops, best of 3: 7.02 µs per loop

def py_sum(arr):
    M, N = arr.shape
    sum = 0.0
    for i in range(M):
        for j in range(N):
            sum += arr[i,j]
    return sum

py_sum(arr2d)   # 1000 loops, best of 3: 228 µs per loop

fast_sum = njit(py_sum)

fast_sum(arr2d) # 1 loop, best of 1: 328 ms per loop
                # The slowest run took 8.35 times longer than the fastest. 
                # This could mean that an intermediate result is being cached.
                # 1000000 loops, best of 3: 1.07 µs per loop

# ¿Impresionado? La primera vez que hemos llamado a la función, Python ha 
# generado el código correspondiente al tipo de datos que le hemos pasado. 

# Podemos verlo aquí:
print(fast_sum.signatures)

# E imprimir el código generado así:
print(fast_sum.inspect_types())

##________ Entendiendo numba: el modo *nopython* ________##

# Como podemos leer en la documentación, [numba tiene dos modos de funcionamiento 
# básicos](http://numba.pydata.org/numba-doc/0.17.0/user/jit.html#nopython): el 
# modo *object* y el modo *nopython*.

    # * El modo *object* genera código que gestiona todas las variables como 
    #   objetos de Python y utiliza la API C de Python para operar con ellas. 
    #   En general en este modo **no habrá ganancias de rendimiento** (e incluso 
    #   puede ir más lento), con lo cual mi recomendación personal es directamente 
    #   no utilizarlo. Hay casos en los que numba puede detectar los bucles y 
    #   optimizarlos individualmente (*loop-jitting*), pero no le voy a prestar 
    #   mucha atención a esto.

    # * El modo *nopython* **genera código independiente de la API C de Python**. 
    #   Esto tiene la desventaja de que no podemos usar todas las características 
    #   del lenguaje, **pero tiene un efecto significativo en el rendimiento**. 
    #   Otra de las restricciones es que **no se puede reservar memoria para 
    #   objetos nuevos**.

# Por defecto numba usa el modo *nopython* siempre que puede, y si no pasa a modo 
# *object*. Nosotros vamos a **forzar el modo nopython** (o «modo estricto» como 
# me gusta llamarlo) porque es la única forma de aprovechar el potencial de numba.

