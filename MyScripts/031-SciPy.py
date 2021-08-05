### Calculate Integrals ###
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

#_______________________________ QUAD INT ____________________________________#
from scipy.integrate import quad # También podemos usar trapz, simps

## Define function ##
def fun(x):
    return x * np.sin(x)

## Plot graph ##
x = np.linspace(0,10,100)
y = fun(x)
with plt.style.context('seaborn-notebook'):
    # título
    plt.title('$y = x sin(x)$', fontsize = 25)
    
    # pintando la línea
    plt.plot(x,y, linewidth = 2)
    
    # pintando el relleno
    x_fill = np.linspace(2,9,100)
    y_fill = fun(x_fill)
    plt.fill_between(x_fill, y_fill, color='gray', alpha=0.5)
    
    # poniendo la cuadrícula
    plt.grid()

## Integrate with quad ##
# Integremos la función en el intervalo [2,9]. Recuerda que esto te calcula la integral, no el area:

value, err = quad(fun, 2, 9)
print("El resultado es: ", value, "con un error de: ", err)

#___________________________SIMPSONS & TRAPEZOID______________________________#
x = np.linspace(2,9,100)

value = integrate.trapz(fun(x), x)

print("El resultado es: ", value)

x = np.linspace(2,9,100)

value = integrate.simps(fun(x), x)

print("El resultado es: ", value)