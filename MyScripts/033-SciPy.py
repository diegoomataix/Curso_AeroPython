###____________________ Interpolation & Curve Fitting ______________________###

# Based on: pybonacci.org/2013/08/15/ajuste-e-interpolacion-unidimensionales-basicos-en-python-con-scipy/

import numpy as np
import matplotlib.pyplot as plt
# plt.ion()

###____________________________ Interpolation  _____________________________###
#_______________________ Airplane Polar Data _______________________#
# Supongamos que tenemos una serie de puntos que representan los datos de un 
# cierto experimento. Como ejemplo, vamos a cargar los datos de la polar de un 
# avión que están en el archivo polar.dat.

datos = np.loadtxt("../data/polar.dat")
C_L = datos[0]
C_D = datos[1]

# Representamos los datos # (pista: usar `mew=2`, "marker edge width 2", para que las cruces se vean mejor):
plt.plot(C_D, C_L, '^', mew=2, label="Datos reales")
plt.xlabel("$C_D$")
plt.ylabel("$C_L$")
plt.legend()
plt.show()

# Identify the stall region # Hallando el índice del máximo valor de 𝐶𝐿 podemos descartar los datos fuera de la región de entrada en pérdida, y para eso necesitamos la función np.argmax
    # tip: argmax function: finds index of max value of a set of data
idx_stall = np.argmax(C_L)
# Identify the C_L_MAX
print((C_L[idx_stall]))

# Representamos los datos dentro y fuera del modelo
plt.plot(C_D[:idx_stall + 1], C_L[:idx_stall + 1], '^', mew=2, label="Datos reales")
plt.plot(C_D[idx_stall + 1:], C_L[idx_stall + 1:], 'x', mfc='none', label="Fuera del modelo")
plt.xlabel("$C_D$")
plt.ylabel("$C_L$")
plt.legend(loc=4)
plt.show()

# Hay dos cosas que nos pueden interesar:
    # Como solo tenemos puntos intermedios, no tenemos posibilidad de evaluar, 
    # por ejemplo, CL para un CD que no esté en los datos. Si interpolamos la 
    # curva ya podemos hacerlo. Sabemos que, fuera de la región de entrada en 
    # pérdida, la polar tiene forma parabólica. Si ajustamos la curva podemos hallar 
    # el CD0 y el k

### Interpolation ###
from scipy import interpolate
# ## easy example with sin(x) ##
x_i = [0.0, 0.9, 1.8, 2.7, 3.6, 4.4, 5.3, 6.2, 7.1, 8.0]
y_i = [0.0, 0.8, 1.0, 0.5, -0.4, -1.0, -0.8, -0.1, 0.7, 1.0]
plt.plot(x_i, y_i, 'd', mew=2)
plt.show()

# # Para crear una función interpolante utilizaremos el objeto InterpolatedUnivariateSpline 
# # del paquete interpolate. A este objeto solo hay que pasarle los puntos de 
# # interpolación y el grado, y generará un spline.
f_interp = interpolate.InterpolatedUnivariateSpline(x_i, y_i, k=2)
# # ¿Cómo obtengo los puntos desde aquí? El resultado que hemos obtenido es una 
# # función y admite como argumento la x.
print(f_interp(np.pi / 2))

x = np.linspace(0, 8)
y_interp = f_interp(x)

plt.plot(x_i, y_i, 'x', mew=2)
plt.plot(x, y_interp)
plt.show()

## Exercise: Crear una función interpolante 𝐶𝐷=𝑓(𝐶𝐿) usando splines de grado 2 
# y representarla. Utiliza solo los datos que resultan de haber eliminado la región 
# de entrada en pérdida. y ten en cuenta que la 𝑥 y la 𝑦 para este caso están 
# cambiadas de sitio. ##
# 1. Crea un polinomio interpolante usando los valores que encajan en el modelo parabólico.
# 2. Crea un dominio de CL entre C_L.min() y C_L.max().
# 3. Halla los valores interpolados de CD en ese dominio.
# 4. Representa la función y los puntos.
f_C_D = interpolate.InterpolatedUnivariateSpline(C_L[:idx_stall + 1], C_D[:idx_stall + 1], k=2) # I put CL first because if im taking a parabolic I am acc seeing the graph rotated 90 deg
C_L_domain = np.linspace(C_L.min(), C_L.max())
C_D_domain = f_C_D(C_L_domain)

with plt.style.context('seaborn-notebook'):
    plt.title('Interpolated Polar Data', fontsize = 25)
    plt.plot(C_D[:idx_stall + 1], C_L[:idx_stall + 1], '^', mew=2, label="Datos reales")
    # plt.plot(C_D[idx_stall + 1:], C_L[idx_stall + 1:], 'x', mfc='none', label="Fuera del modelo")
    plt.plot(C_D_domain, C_L_domain, label="Interpolated data", color="purple")
    plt.xlabel("$C_D$")
    plt.ylabel("$C_L$")
    plt.legend(loc=4)
    plt.grid()
    plt.show()

#_______________________ Runge Phenomenon _______________________#
def runge(x):
    return 1 / (1 + x ** 2)

# Número de nodos
N = 11  # Nodos de interpolación

# Seleccionamos los nodos
xp = np.linspace(-5, 5, N)   # -5, -4, -3, ..., 3, 4, 5
fp = runge(xp)

# Seleccionamos la x para interpolar
x = np.linspace(-5, 5, 200)
# Calculamos el pol interp de Lagrange
lag_pol = interpolate.lagrange(xp, fp)
y = lag_pol(x)

with plt.style.context('seaborn-notebook'):
    plt.plot(x, y, label='interpolation')
    plt.plot(xp, fp, 'o', label='samples')
    plt.plot(x, runge(x), label='real')
    plt.legend(loc='upper center')
    plt.show()

# importamos el polinomio de chebychev #
from numpy.polynomial import chebyshev
N = 11  # Nodos de interpolación

coeffs_cheb = [0] * N + [1]  # Solo queremos el elemento 11 de la serie

T11 = chebyshev.Chebyshev(coeffs_cheb, [-5, 5])
xp_ch = T11.roots()

fp = runge(xp_ch)

x = np.linspace(-5, 5, 200)

lag_pol = interpolate.lagrange(xp_ch, fp)
# lag_pol = interpolate.InterpolatedUnivariateSpline(xp_ch, fp, k=2) # Just to check

y = lag_pol(x)
with plt.style.context('seaborn-notebook'):
    plt.plot(x, y, label='interpolation')
    plt.plot(xp_ch, fp, 'o', label='samples')
    plt.plot(x, runge(x), label='real')
    plt.legend()
    plt.show()
    
###_______________________________ Fitting _________________________________###
 # El ajuste funciona de manera totalmente distinta: obtendremos una curva que no
 # tiene por qué pasar por ninguno de los puntos originales, pero que a cambio 
 # tendrá una expresión analítica simple.
from scipy.optimize import curve_fit
# # ## easy example with random quadratic function ##
#  # Vamos otra vez a generar unos datos para ver cómo funcionaría, del tipo:
#  # $$y(x) = x^2 - x + 1 + \text{Ruido}$$
x_i = np.linspace(-2, 3, num=10)
y_i = x_i ** 2 - x_i + 1 + 0.5 * np.random.randn(10) # np.random.randn(10) Creates an array with 10 components that are random numbers
plt.plot(x_i, y_i, 'x', mew=2)
plt.show()

#  # Vamos a utilizar la función polynomial.polyfit, que recibe los puntos de 
#  # interpolación y el grado del polinomio. El resultado serán los coeficientes 
#  # del mismo, en orden de potencias crecientes.
def poldeg2(x, a, b, c):
    return a * x**2 + b * x + c

val, cov = curve_fit(poldeg2, x_i, y_i)
a, b, c = val

x = np.linspace(-2, 3)

y_fit = poldeg2(x, a, b, c)

with plt.style.context('seaborn-notebook'):
    l, = plt.plot(x, y_fit)
    plt.plot(x_i, y_i, 'x', mew=2, c=l.get_color())
    plt.grid()
    plt.show()

## Exercise: Si modelizamos la polar como: CD=CD0+k*CL**2, 
# hallar los coeficientes CD0 y k ##
def model(x, A, C):
    return A*x**2 + C

popt, lqdata = curve_fit(model, C_L[:idx_stall+1], C_D[:idx_stall+1])
A, B = popt
# To compute one standard deviation errors on the parameters use:
perr = np.sqrt(np.diag(lqdata))

x = np.linspace(-1.5, 1.5, 50)
y = model(x, A, B)

with plt.style.context('seaborn-notebook'):
    plt.plot(y, x)
    plt.plot(C_D[:idx_stall + 1], C_L[:idx_stall + 1], 'x', mew=2, label="Datos reales")
    plt.plot(C_D[idx_stall + 1:], C_L[idx_stall + 1:], 'o', mfc='none', label="Fuera del modelo")
    plt.xlabel("$C_D$")
    plt.ylabel("$C_L$")
    plt.legend(loc=4)
    plt.grid()  
    plt.show()

