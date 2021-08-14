###_________________________ Lotka-Volterra Model __________________________###
###                         Prey - Predator Model                           ###
# Las ecuaciones de Lotka-Volterra son un modelo biomatemático que pretende responder 
# a estas cuestiones prediciendo la dinámica de las poblaciones de presa y depredador 
# bajo una serie de hipótesis:
    # * El ecosistema está aislado: no hay migración, no hay otras especies presentes, 
    #   no hay plagas...
    # * La población de presas en ausencia de depredadores crece de manera exponencial: 
    #   la velocidad de reproducción es proporcional al número de individuos. 
    #   Las presas sólo mueren cuando son cazadas por el depredador.
    # * La población de depredadores en ausencia de presas decrece de manera exponencial.
    # * La población de depredadores afecta a la de presas haciéndola decrecer de 
    #   forma proporcional al número de presas y depredadores (esto es como decir 
    #   de forma proporcional al número de posibles encuentros entre presa y depredador).
    # * La población de presas afecta a la de depredadores también de manera 
    #   proporcional al número de encuentros, pero con distinta constante de 
    #   proporcionalidad (dependerá de cuanto sacien su hambre los depredadores 
    #   al encontrar una presa).

# Se trata de un sistema de dos ecuaciones diferenciales de primer orden, acopladas, 
# autónomas y no lineales:
    
    # $$ \frac{dx}{dt} = \alpha x - \beta x y $$
    # $$ \frac{dy}{dt} = -\gamma y + \delta y x $$
    
# donde x es el número de presas e y es el número de depredadores. 
# Los parámetros son constantes positivas que representan:
    # * $\alpha$: tasa de crecimiento de las presas.
    # * $\beta$: éxito en la caza del depredador.
    # * $\gamma$: tasa de decrecimiento de los depredadores.
    # * $\delta$: éxito en la caza y cuánto alimenta cazar una presa al depredador.
#_____________________________________________________________________________#
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# System of 1st order ODEs 
def df_dt(x, t, a, b, c, d):
    
    dx = a * x[0] - b * x[0] * x[1]
    dy = - c * x[1] + d * x[0] * x[1]
    
    return np.array([dx, dy])

# Parameters
a = 0.1
b = 0.02
c = 0.3
d = 0.01

# Initial Conditions
x0 = 40
y0 = 9
conds_iniciales = np.array([x0, y0])

# Conditions for integration
tf = 200
N = 800
t = np.linspace(0, tf, N)

# Solve the equation
solucion = odeint(df_dt, conds_iniciales, t, args=(a, b, c, d))

# Plot population in terms of time
plt.style.use('seaborn-talk')

plt.figure("Temporal Evolution", figsize=(8,5))
plt.title("Temporal Evolution")
plt.plot(t, solucion[:, 0], label='Prey')
plt.plot(t, solucion[:, 1], label='Predator')
plt.xlabel('Time')
plt.ylabel('Population')
plt.grid()
plt.legend()
plt.show()

# Plot Prey pop. in terms of Predator pop.
plt.figure("Preys vs Predators", figsize=(8,5))
plt.plot(solucion[:, 0], solucion[:, 1], 'r')
plt.xlabel('Prey')
plt.ylabel('Predator')
plt.grid()
plt.show()

# Plot phase map and direction field

# Podemos pintar el campo de direcciones de nuestras ecuaciones usando la función 
# quiver. El tamaño de las flechas se ha normalizado para que todas tengan la misma 
# longitud y se ha usado un colormap para representar el módulo.
x_max = np.max(solucion[:,0]) * 1.05
y_max = np.max(solucion[:,1]) * 1.05

x = np.linspace(0, x_max, 25)
y = np.linspace(0, y_max, 25)

xx, yy = np.meshgrid(x, y)
uu, vv = df_dt((xx, yy), 0, a, b, c, d)
norm = np.sqrt(uu**2 + vv**2)
uu = uu / norm
vv = vv / norm

plt.figure("Direction field", figsize=(8,5))
plt.quiver(xx, yy, uu, vv, norm, cmap=plt.cm.gray)
plt.plot(solucion[:, 0], solucion[:, 1], 'r')
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.xlabel('Preys')
plt.ylabel('Predators')
plt.grid()
plt.show()

# Plot direction field + Pop vs time
n_max = np.max(solucion) * 1.10

fig, ax = plt.subplots(1,2)

fig.set_size_inches(12,5)

ax[0].quiver(xx, yy, uu, vv, norm, cmap=plt.cm.gray)
ax[0].plot(solucion[:, 0], solucion[:, 1], lw=2, alpha=0.8)
ax[0].set_xlim(0, x_max)
ax[0].set_ylim(0, y_max)
ax[0].set_xlabel('Preys')
ax[0].set_ylabel('Predators')

ax[1].plot(t, solucion[:, 0], label='Preys')
ax[1].plot(t, solucion[:, 1], label='Predators')
ax[1].legend()
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Population')
plt.show()

##_______________________ Effect of initial conditions ______________________##
# Se puede demostrar que a lo largo de las líneas del mapa de fases, como la que 
# hemos pintado antes, se conserva la cantidad:
    # $$ C = \alpha \ln{y} - \beta y + \gamma \ln{x} -\delta x $$
# Por tanto, pintando un `contour` de esta cantidad podemos obtener la solución 
# para distintos valores iniciales del problema.

def C(x, y, a, b, c, d):
    return a * np.log(y) - b * y + c * np.log(x) - d * x

x = np.linspace(0, x_max, 100)
y = np.linspace(0, y_max, 100)
xx, yy = np.meshgrid(x, y)
constant = C(xx, yy, a, b, c, d)

plt.figure('Various solutions', figsize=(8,5))
plt.contour(xx, yy, constant, 50, cmap=plt.cm.Blues)
plt.xlabel('Preys')
plt.ylabel('Predators')
plt.grid()
plt.show()

# Vemos que estas curvas se van haciendo cada vez más y más pequeñas, hasta que, 
# en nuestro caso, colapsarían en un punto en torno a $(30,5)$. Se trata de un 
# punto de equilibrio o punto crítico; si el sistema lo alcanzase, no evolucionaría 
# y el número de cebras y leones sería constante en el tiempo. El otro punto crítico 
# de nuestro sistema es el $(0,0)$. Analizándolos matemáticamente se obtiene que:

# El punto crítico situado en $(0,0)$ es un punto de silla. Al tratarse de un punto 
# de equilibrio inestable la extinción de cualquiera de las dos especies en el 
# modelo sólo puede conseguirse imponiendo la condición inicial nula.

# El punto crítico situado en $(gamma/delta,alpha/beta)$ es un centro (en este 
# caso los autovalores de la matriz del sistema linealizado son ambos imaginarios
# puros, por lo que a priori no se conoce su estabilidad).

fig, ax = plt.subplots(1,2)

fig.set_size_inches(12,5)

ax[0].plot(solucion[:, 0], solucion[:, 1], lw=2, alpha=0.8)
ax[0].scatter(c/d, a/b)
levels = (0.5, 0.6, 0.7, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.775, 0.78, 0.781)
ax[0].contour(xx, yy, constant, levels, colors='blue', alpha=0.3)
ax[0].set_xlim(0, x_max)
ax[0].set_ylim(0, y_max)
ax[0].set_xlabel('presas')
ax[0].set_ylabel('depredadores')

ax[1].plot(t, solucion[:, 0], label='presa')
ax[1].plot(t, solucion[:, 1], label='depredador')
ax[1].legend()
ax[1].set_xlabel('tiempo')
ax[1].set_ylabel('población')
plt.show()

##___________________________ Improving the model ___________________________##
# Como se puede observar, este modelo tiene algunas deficiencias propias de su 
# simplicidad y derivadas de las hipótesis bajo las que se ha formulado. Una 
# modificación razonable es cambiar el modelo de crecimiento de las presas en 
# ausencia de depredadores, suponiendo que en vez de aumentar de forma exponencial, 
# lo hacen según una [función logística](http://es.wikipedia.org/wiki/Funci%C3%B3n_log%C3%ADstica). 
# Esta curva crece de forma similar a una exponencial al principio, moderándose
# después y estabilizándose asintóticamente en un valor:

def logistic_curve(t, a=1, m=0, n=1, tau=1):
    e = np.exp(-t / tau)
    return a * (1 + m * e) / (1 + n * e) 

x_ = np.linspace(0,10)
plt.figure('función logística', figsize=(8,5))
plt.plot(x_, logistic_curve(x_, 1, m=10, n=100, tau=1))
plt.grid()
plt.plot()

# Podemos observar como esta curva crece de forma similar a una exponencial al 
# principio, moderándose después y estabilizándose asintóticamente en un valor. 
# Este modelo de crecimiento representa mejor las limitaciones en el número de 
# presas debidas al medio (falta de alimento, territorio...). Llevando este modelo 
# de crecimiento a las ecuaciones originales se tiene un nuevo sistema en el que 
# interviene un parámetro más:
    # $$ \frac{dx}{dt} = (\alpha x - r x^2) - \beta x y $$
    # $$ \frac{dy}{dt} = -\gamma y + \delta y x $$

def df_dt_logistic(x, t, a, b, c, d, r):
    
    dx = a * x[0] - r * x[0]**2 - b * x[0] * x[1]
    dy = - c * x[1] + d * x[0] * x[1]
    
    return np.array([dx, dy])

# Parámetros
a = 0.1
b = 0.02
c = 0.3
d = 0.01
r = 0.001

# Condiciones iniciales
x0 = 40
y0 = 9
conds_iniciales = np.array([x0, y0])

# Condiciones para integración
tf = 200
N = 800
t = np.linspace(0, tf, N)

# Solution
solucion_logistic = odeint(df_dt_logistic, conds_iniciales, t, args=(a, b, c, d, r))

n_max = np.max(solucion) * 1.10

fig, ax = plt.subplots(1,2)

fig.set_size_inches(12,5)

x_max = np.max(solucion_logistic[:,0]) * 1.05
y_max = np.max(solucion_logistic[:,1]) * 1.05

x = np.linspace(0, x_max, 25)
y = np.linspace(0, y_max, 25)

xx, yy = np.meshgrid(x, y)
uu, vv = df_dt_logistic((xx, yy), 0, a, b, c, d, r)
norm = np.sqrt(uu**2 + vv**2)
uu = uu / norm
vv = vv / norm

ax[0].quiver(xx, yy, uu, vv, norm, cmap=plt.cm.gray)
ax[0].plot(solucion_logistic[:, 0], solucion_logistic[:, 1], lw=2, alpha=0.8)
ax[0].set_xlim(0, x_max)
ax[0].set_ylim(0, y_max)
ax[0].set_xlabel('presas')
ax[0].set_ylabel('depredadores')

ax[1].plot(t, solucion_logistic[:, 0], label='presa')
ax[1].plot(t, solucion_logistic[:, 1], label='depredador')
ax[1].legend()
ax[1].set_xlabel('tiempo')
ax[1].set_ylabel('población')
plt.grid()
plt.show()

# En este caso se puede observar como el comportamiento deja de ser periódico. 
# El punto crítico que antes era un centro, se convierte en un atractor y la 
# solución tiende a estabilizarse en un número fijo de presas y depredadores.
