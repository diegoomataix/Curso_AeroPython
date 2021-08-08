###_____________________ Ordinary Differential Eqs _________________________### 
import numpy as np
import matplotlib.pyplot as plt
# Para integrar EDOs vamos a usar la función `odeint` del paquete `integrate`, 
# que permite integrar sistemas del tipo:
    # $$ \frac{d\mathbf{y}}{dt}=\mathbf{f}\left(\mathbf{y},t\right)$$
# con condiciones iniciales $\mathbf{y}(\mathbf{0}) = \mathbf{y_0}$.
from scipy.integrate import solve_ivp
# **¡Importante!**: La función del sistema recibe como primer argumento 𝐲
# (un array) y como segundo argumento el instante t (un escalar). Esta convención 
# va exactamente al revés que en MATLAB y si se hace al revés obtendremos errores 
# o, lo que es peor, resultados incorrectos.

##_________________________ 1st order ODE ___________________________##
# Vamos a integrar primero una EDO elemental, cuya solución ya conocemos:
    # $$y' + y = 0$$
# $$f(y, t) = \frac{dy}{dt} = -y$$
def f(t,y):
    return np.array([-y])
# Initial conditions
y0 = np.array([1])
tini = 0
tfin = 3
# Integrating and representing the solution
sol = solve_ivp(f, (tini, tfin), y0)
# plt.plot(sol.t, sol.y[0,:], 'o-') 
# Pero, ¿cómo se han seleccionado los puntos en los que se calcula la solución? 
# El solver los ha calculado por nosotros. Si queremos tener control sobre estos 
# puntos, podemos pasar de manera explícita el vector de tiempos:
time = np.linspace(tini, tfin, 30)
sol_2 = solve_ivp(f, (tini, tfin), y0, t_eval=time)
# plt.plot(sol_2.t, sol_2.y[0, :], 'd-')
# El solver siempre da los pasos que considere necesarios para calcular la solución,
# pero sólo guarda los que nosotros le indicamos.
print(f"function evaluations in sol 1: {sol.nfev}")
print(f"function evaluations in sol 2: {sol_2.nfev}")
# De hecho podemos usar la salida densa para obtener la solución en un punto cualquiera:
sol_3 = solve_ivp(f, (tini, tfin), y0, dense_output=True)
print(sol_3.sol([1.14567, 2, 6]))
t = np.linspace(tini, tfin, 45)
y = sol_3.sol(t)
# plt.plot(t, y[0, :], 'x-')

##_________________________ Higher order ODE ___________________________##
# Tendremos que acordarnos ahora de cómo reducir las ecuaciones de orden. De nuevo, 
# vamos a probar con un ejemplo académico:
    # $$y + y'' = 0$$
    # $$\mathbf{y} \leftarrow \pmatrix{y \\ y'}$$
    # $$\mathbf{f}(\mathbf{y}) = \frac{d\mathbf{y}}{dt} =  \pmatrix{y \\ y'}' = 
        # \pmatrix{y' \\ y''} = \pmatrix{y' \\ -y}$$
def f2(t,y):
    return np.array([y[1], -y[0]])
# init conditions and domain
t0=0
t1=10
t = np.linspace(t0,t1)
y0 = np.array([1.0,0.0])
# solver
sol = solve_ivp(f2, (t0, t1), y0, t_eval=t)
with plt.style.context('seaborn-notebook'):
    plt.plot(t, sol.y[0, :], label='$y$')
    plt.plot(t, sol.y[1, :], '--k', label='$\dot{y}$')
    plt.legend()
    plt.grid()
