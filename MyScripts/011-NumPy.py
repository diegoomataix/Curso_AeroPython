import numpy as np


### 1) Homogeneidad de tipo: ###
lista = [ 1, 1+2j, True, 'aerodinamica', [1, 2, 3] ]
#print(lista)

#  En la lista cada elemento conserva su tipo


array = np.array([ 1, 1+2j, True, 'aerodinamica'])
#print(array)

# En array todos han de tener el mismo y NumPy ha considerado que todos van a ser string.

### 2) Tamaño fijo en el momento de la creación: ###
# print(id(lista))
lista.append('fluidos')
# print(lista)
# print(id(lista))

# print(id(array))
array = np.append(array, 'fluidos')
# print(array)
# print(id(array))

### 3) Eficiencia ###
#  Los arrays realizan una gestión de la memoria mucho más eficiente que mejora el rendimiento.

##### EXERCISE #####
# Para recordar los primeras lecciones vamos a implementar nuestra propia función 
# linspace usando un bucle (estilo FORTRAN) y usando una list comprehension (estilo pythonico). 
# Después compararemos el rendimiento comparado con la de NumPy

def my_linspace_FORTRAN(start, stop, number=50):
    x = np.empty(number)
    step = (stop - start) / (number - 1)
    for ii in range(number):
        x[ii] = ii * step
    x += start
    return x

def my_linspace_PYTHONIC(start, stop, number=50):
    step = (stop - start) / (number - 1)
    x = np.array([ii * step  for ii in range(number)]) #esto es una list comprehension
    x += start
    return x

# %%timeit
a = np.linspace(0,100,1000000)
# %%timeit
b = my_linspace_FORTRAN(0,100,1000000)
# %%timeit
c = my_linspace_PYTHONIC(0,100,1000000)