###________________________ Non-Lineal-Equations ___________________________### 
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# La ayuda de este paquete es bastante larga (puedes consultarla también en 
# http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html). 
# El paquete optimize incluye multitud de métodos para optimización, ajuste de 
# curvas y búsqueda de raíces. Vamos a centrarnos ahora en la búsqueda de raíces 
# de funciones escalares. Para más información puedes leer 
# http://pybonacci.org/2012/10/25/como-resolver-ecuaciones-algebraicas-en-python-con-scipy/

# **Nota**: La función `root` se utiliza para hallar soluciones de *sistemas* de 
# ecuaciones no lineales así que obviamente también funciona para ecuaciones escalares. 
# No obstante, vamos a utilizar las funciones `brentq` y `newton` para que el método 
# utilizado quede más claro.

# Hay básicamente dos tipos de algoritmos para hallar raíces de ecuaciones no lineales:

# * Aquellos que operan en un intervalo $[a, b]$ tal que $f(a) \cdot f(b) < 0$. 
# Más lentos, convergencia asegurada.
# * Aquellos que operan dando una condición inicial $x_0$ más o menos cerca de 
# la solución. Más rápidos, convergencia condicionada.

# De los primeros vamos a usar la función `brentq` (aunque podríamos usar `bisect`) 
# y de los segundos vamos a usar `newton` (que en realidad engloba los métodos 
# de Newton y de la secante).

##_________________________ Example ___________________________##
# $\ln{x} = \sin{x} \Rightarrow F(x) \equiv \ln{x} - \sin{x} = 0$
# Lo primero que tengo que hacer es definir la ecuación, que matemáticamente 
# será una función $F(x)$ que quiero igualar a cero.
def F(x):
    return np.log(x) - np.sin(x)
# Para hacernos una idea de las posibles soluciones siempre podemos representar 
# gráficamente esa función:
# x = np.linspace(0, 10, num=100)
# with plt.style.context('seaborn-notebook'):
#     plt.plot(x, F(x), 'k', lw=2, label="$F(x)$")
#     plt.plot(x, np.log(x), label="$\log{x}$")
#     plt.plot(x, np.sin(x), label="$\sin{x}$")
#     plt.plot(x, np.zeros_like(x), 'k--')
#     plt.legend(loc=4)
#     plt.grid()
# Y utilizando por ejemplo el método de Brent en el intervalo [0,3]:
# print(optimize.brentq(F, 0, 3))

##_________________________ Exercise ___________________________##
# Obtener por ambos métodos (newton y brentq) una solución a la ecuación 
# tanx=x distinta de x=0. Visualizar el resultado.
## Argumentos extra ##
# Nuestras funciones siempre tienen que tomar como primer argumento la incógnita,
# el valor que la hace cero. Si queremos incluir más, tendremos que usar el argumento 
# `args` de la funciones de búsqueda de raíces. Este patrón se usa también en otras 
# partes de SciPy, como ya veremos.

# Vamos a resolver ahora una ecuación que depende de un parámetro:
    # $$\sqrt{x} + \log{x} = C$$.
def G(x, C):
    return C - np.sqrt(x) - np.log(x)
# **Nuestra incógnita sigue siendo $x$**, así que debe ir en primer lugar. 
# El resto de parámetros van a continuación, y sus valores se especifican a la 
# hora de resolver la ecuación usando `args`:
# print(optimize.newton(G, 2.0, args=(2,)))

##_________________________ Compressible Flow ___________________________##
# Esta es la relación isentrópica entre el número de Mach $M(x)$ en un conducto 
# de área $A(x)$:
    # $$ \frac{A(x)}{A^*} = \frac{1}{M(x)} \left( \frac{2}{1 + \gamma} \left( 1 + 
    # \frac{\gamma - 1}{2} M(x)^2 \right) \right)^{\frac{\gamma + 1}{2 (\gamma - 1)}}$$
# Para un conducto convergente:
    # $$ \frac{A(x)}{A^*} = 3 - 2 x \quad x \in [0, 1]$$
# Hallar el número de Mach en la sección 𝑥=0.9.
def A(x):
    return 3 - 2 * x
x = np.linspace(0, 1)
area = A(x)
r = np.sqrt(area / np.pi)
# plt.fill_between(x, r, -r, color="#ffcc00")
# ¿Cuál es la función $F$ ahora? Hay dos opciones: definir una función $F_{0.9}(M)$ 
# que me da el número de Mach en la sección $0.9$ o una función $F(M; x)$ con la 
# que puedo hallar el número de Mach en cualquier sección. 

# Para resolver la ecuación utiliza el método de Brent (bisección). ¿En qué intervalo 
# se encontrará la solución? ¡Si no te haces una idea es tan fácil como pintar 
# la función $F$!
def F(M, x, g):
    return A(x) - (1 / M) * ((2 / (1 + g)) * (1 + (g - 1) / 2 * M ** 2)) ** ((g + 1) / (2 * (g - 1))) 

# print(optimize.brentq(F, 0.01, 1, args=(0.9, 1.4)))

##_______________________________ Kepler law ________________________________##
# Representar la ecuación de Kepler
    # $$M = E - e \sin E$$

# que relaciona dos parámetros geométricos de las órbitas elípticas, la anomalía 
# media $M$ y la anomalía excéntrica $E, para los siguientes valores de excentricidad:
    # * Tierra: $0.0167$
    # * Plutón: $0.249$
    # * Cometa Holmes: $0.432$
    # * 28P/Neujmin: $0.775$
    # * Cometa Halley: $0.967$

# Para ello utilizaremos el método de Newton (secante).
# 1- Define la función correspondiente a la ecuación de Kepler, que no solo es 
# una ecuación implícita sino que además depende de un parámetro. ¿Cuál es la incógnita?
def Kepler(E, e, M):
    return M - E + e * np.sin(E)
# 2- Como primer paso, resuélvela para la excentricidad terrerestre y anomalía 
# media $M = 0.3$. ¿Qué valor escogerías como condición inicial?
print(optimize.newton(Kepler, 0.3, args=(0.0167, 0.3)))
# 3- Como siguiente paso, crea un dominio (`linspace`) de anomalías medias entre 
# $0$ y $2 \pi$ y resuelve la ecuación de Kepler con excentricidad terrestre para 
# todos esos valores. Fíjate que necesitarás un array donde almacenar las soluciones. 
# Representa la curva resultante.
N = 500

# M = np.linspace(0, 2 * np.pi, N)
# sol = np.zeros_like(M)

# for ii in range(N):
#     sol[ii] = optimize.newton(Kepler, sol[ii - 1], args=(0.249, M[ii]))
# plt.plot(M, sol)
# 4- Como último paso, solo tienes que meter parte del código que ya has escrito 
# en un bucle que cambie el valor de la excentricidad 5 veces. 
M = np.linspace(0, 2 * np.pi, N)
sol = np.zeros_like(M)

plt.figure(figsize=(6, 6))

for ee in 0.0167, 0.249, 0.432, 0.775, 0.967:
    # Para cada valor de excentricidad sobreescribimos el array sol
    for ii in range(N):
        sol[ii] = optimize.newton(Kepler, sol[ii - 1], args=(ee, M[ii]))
    with plt.style.context('seaborn-notebook'):
        plt.plot(M, sol)
with plt.style.context('seaborn-notebook'):
    plt.xlim(0, 2 * np.pi)
    plt.ylim(0, 2 * np.pi)
    plt.xlabel("$M$", fontsize=15)
    plt.ylabel("$E$", fontsize=15)
    plt.gca().set_aspect(1)
    plt.grid(True)
    plt.legend(["Earth", "Pluto", "Comet Holmes", "28P/Neujmin", "Halley's Comet"], loc=2)
    plt.title("Kepler's equation solutions", fontsize=15)
