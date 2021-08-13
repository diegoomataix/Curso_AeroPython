###_______________________ FelixBaumgartner Jump ___________________________### 
###_____________________ Ordinary Differential Eqs _________________________### 
# EDO: (ecuación que gobierna la caída de Felix es:)
    # $$\displaystyle m \frac{d^2 y}{d t^2} = -m g + D$$ # 
# With:
    # $$D = \frac{1}{2} \rho v^2 C_D A$$
# Where:
    # * $m$ es la masa de Félix y la tomaremos $m = 80~\text{kg}$,
    # * $\rho$ es la densidad del aire **y depende de la altura**,
    # * $v = |\dot{y}|$ es la velocidad,
    # * $C_D$ es el coeficiente de rozamiento, que tomaremos* $C_D = 0.4$, y
    # * $A$ es un área de referencia y tomaremos $A = 1~\text{m}^2$.
# Source: http://fisicadepelicula.blogspot.com.es/2012/10/la-fisica-del-salto-baumgartner.html
# Además, necesitaremos la altura inicial $h_0 = 39000 m$.
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
# from scipy.integrate import solve_ivp # Different solver
# from numpy.testing import assert_almost_equal

##_________________________ Temp ISA ___________________________##
# $$T(h) = \begin{cases} T_0 + \lambda h & 0 <= h <= 11000 \\ T(11000) & 11000 < h \end{cases}
# \\ ~\\ T_0 = 288.16 K \\
# \lambda = -6.5 \cdot 10^{-3}~\text{K/m}$$

# **¡Importante!** Si utilizas condicionales para comprobar las capas de la atmósfera, 
# seguramente tus funciones fallarán si las quieres representar utilizando un `linspace`. 
# Para estos casos es mejor utilizar la función `np.select`:
def T_ISA(h):
    """Temperature as a function of altitude using the ISA.

    Arguments
    ----------
    h : Altitude in metres.

    Returns
    --------
    T : Temperature in Kelvin.

    """
    # Con esta línea convertimos la entrada a un array
    h = np.asarray(h)
    # Initial values
    T0 = 288.16  # K
    ll = -6.5e-3 # K/m
    ## One way to do it (without h=np.asarray(h)) ##
    # if 0 <= h <= 11000:
    #     T = T0 + ll*h
    # elif 11000 < h:
    #     T = T0 + ll*11000
    ## Another way to do it with h as array ##
    # 0 <= h <= 110000 no funciona para arrays
    T1 = T0 + ll * h
    T2 = T0 + ll * 11000
    T = np.select([(0 <= h) & (h <= 11000), 11000 < h], [T1, T2])
    return T
# Si quieres comprobar que tus funciones hacen lo que deben, puedes ejecutar estos tests:
# print(assert_almost_equal(T_ISA(0), 288.16))
# print(assert_almost_equal(T_ISA(11000), 216.66))

##_________________________ Rho ISA ___________________________##
# $$ \rho(h) = \begin{cases} \rho_0 \left( \frac{T}{T_0} \right)^{-\frac{g}{\lambda R} - 1} 
# & 0 <= h <= 11000 \\ \rho(11000)~e^{\frac{-g(z - 11000)}{R T}} & 11000 < h <= 20000 
# \end{cases} $$
# $$\rho_0 = 1.225~\text{[SI]} \\
# R = 287~\text{[SI]}$$
def rho_ISA(h):
    """Density (rho) as a function of altitude using the ISA.

    Arguments
    ----------
    h : Altitude in metres.

    Returns
    --------
    rho : Density in [SI].

    """
    h = np.asarray(h)
    # Initial values
    T0 = 288.16  # K
    ll = -6.5e-3 # K/m
    rho0 = 1.225 # kg / m3
    g = 9.81     # m / s2
    R = 287      # [SI]
    rho1 = rho0 * (T_ISA(h) / T0) ** (-g / (ll * R) - 1)
    rho2 = rho0 * (T_ISA(11000) / T0) ** (-g / (ll * R) - 1) * np.exp(-g * (h - 11000) / (R * T_ISA(h)))
    rho = np.select([(0 <= h) & (h <= 11000), 11000 < h], [rho1, rho2])
    return rho

##_________________________ EDO ___________________________##
# System Equation
def f(y, t):
    g = 9.8  # m / s2
    C_D = 0.4
    A = 1.0  # m^2
    m = 80  # kg
    return np.array([
        y[1],
        -g + rho_ISA(y[0]) * y[1] ** 2 * C_D * A / (2 * m)
    ])
# Initial Conditions
y0 = np.array([39000, 0])
# Time vector
t = np.linspace(0, 250)
# Integrate the equation
sol = odeint(f, y0, t)
pos = sol[:, 0]  # Primera columna: posición
vel = sol[:, 1]  # Segunda columna: velocidad
# Representing the solution
with plt.style.context('seaborn-notebook'):
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(6, 6))
    line, = axes[0].plot(t, pos / 1e3, label="Position $y$")
    axes[0].set_ylabel("Position [km]")
    axes[1].plot(t, vel, '--', color=line.get_color(), label="Velocity $\dot{y}$")
    axes[1].set_ylabel("Velocity [m/s]")
    # axes[1].set_xlabel("Time (s)")
    axes[0].legend()
    axes[1].legend()
    axes[0].set_title("Felix Baumgartner free fall")
    axes[0].grid()
    axes[1].grid()
    fig.tight_layout()

##_________________________ Sound Barrier _________________________##
# La velocidad del sonido en el aire variará también, y lo hará de esta forma:
    # $$M = \frac{v}{c}$$
# where: $$c = \sqrt{\gamma R T}$$

# Como paso final, representa 𝑀 en función de 𝑡 y en la misma gráfica incluye una
# línea horizontal de trazo discontinuo donde 𝑀=1
gamma = 1.4
R = 287.0  # [SI]
c = np.sqrt(gamma * R * T_ISA(pos))

M = np.abs(vel) / c

with plt.style.context('seaborn-notebook'):
    plt.plot(t, M, 'r', label="Mach Number $\mathrm{M}$")
    plt.plot(t, np.ones_like(t), 'k--')
    plt.ylabel('Mach number')
    plt.xlabel('Time [s]')
    # plt.title("Mach number")
    plt.legend()
    plt.grid()