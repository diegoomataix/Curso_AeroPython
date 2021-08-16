###_____________________________ Field Theory ______________________________### 
import numpy as np
import matplotlib.pyplot as plt

##_______________________ Drawing a circumference ______________________##
# Como paso previo a la creación de un anillo circular crearemos una circunferencia, 
# ya que es un ejemplo más sencillo

# 1. __Creamos `N` puntos de la circunferencia__ de modo que __en `Xc` estén las
# coordenadas $x$ y en `Yc` estén las coordenadas $y$__ de los puntos que la 
# forman. Controla el número de puntos mediante un parámetro que se llame `N_puntos`.
    #     $$X_c = x0 + R·cos(\theta)$$
    #     $$Y_c = y0 + R·sin(\theta)$$
# 2. Una vez hayas obtenido los dos arrays `Xc` e `Yc`, __píntalos mediante un 
# `scatter`__ para comprobar que todo ha ido bien.
# 3. Pinta también el __centro de la circunferencia__.

# El resultado debería ser parecido a esto:
    
# Número de puntos de la circunferencia
N_puntos = 100

# Centro
x0 = 0
y0 = 1

#Radio
R = 2 

# Se barre un ángulo de 0 a 2 pi
theta = np.linspace(0, 2*np.pi, N_puntos)

# Se crean las coordenadas del los puntos
# de la circunferencia
Xc = x0 + R * np.cos(theta)
Yc = y0 + R * np.sin(theta)

# Lo representamos
plt.figure("Circumference", figsize=(5,5))
plt.title('Circumference', {'fontsize':20})
plt.scatter(Xc, Yc)
plt.scatter(x0, y0, color='orange', marker='x', s=100)
plt.grid()
plt.show()

##________________________ 2D plate with a ring shape _______________________##
# Radial Direction:
Nr = 20  # Número de puntos en la dirección radial.
R_min = 1  # m.
R_max = 5  # m.

# Tangencial Direction:
Nt = 180   # Número de puntos en la dirección tangencial.

r = np.linspace(R_min, R_max, Nr)
t = np.linspace(0, 2*np.pi , Nt)

# Crear la malla:
xx =  r * np.cos(t).reshape([-1, 1])
yy = r * np.sin(t).reshape([-1, 1])

#pintamos la malla para verla
plt.figure(figsize=(6, 6))
plt.plot(xx.flatten(), yy.flatten(), 'k.')
plt.show()

##________________________ Temperature distribution _________________________##
# Imaginemos que nuestra placa se somete a una distribución de temperaturas según 
# la función:
    # $$T = -  \log(\sqrt{x^2 + y^2}) $$
# Define una función que dados unos valores de x e y, devuelva el valor de la 
# temperatura en el punto.

def temperature_distribution(x, y):
    """Calculate the temperature for a point defined by
    its cartesian coordinates: x, y.
    """
    return -np.log(np.sqrt(x**2 + y**2))

# Calculate temperature values
temps = temperature_distribution(xx, yy)

# Show
plt.figure(figsize=(6, 6))
plt.title('Distribución de temperaturas', fontsize=20)  
plt.contour(xx, yy, temps, 10, colors='black', linestyles='-')
plt.contourf(xx, yy, temps, 100, cmap=plt.cm.Spectral) # matplotlib trae por defecto muchos mapas de colores. En las SciPy Lecture Notes dan una lista de todos ellos (http://scipy-lectures.github.io/intro/matplotlib/matplotlib.html#colormaps)
plt.colorbar(fraction=0.045)
plt.gca().set_aspect(1)
plt.show()

# Como más adelante calcularemos el gradiente, quizá sea útil representar la 
# temperatura en la placa como una superficie:
from mpl_toolkits.mplot3d import Axes3D

plt.figure('Surface')
ax = plt.subplot(projection='3d')
ax.plot_surface(xx, yy, temps, rstride=5, cstride=5, cmap=plt.cm.Spectral)
plt.title('Surface Plot')
plt.show()
# Más ejemplos de gráficas en 3d en http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

##___________________ Temperature Gradient distribution _____________________##
# En primer lugar definiremos una función que calcule el gradiente en cualquier 
# punto x, y:
def temp_gradient(x, y):
    """Calculate the temperature gradient for a point
    defined by its cartesian coordinates: x, y.
    """    # Could also use SymPy to calculate derivative tbh
    fx = -x / (x**2 + y**2)
    fy = -y /  (x**2 + y**2)
    return fx, fy    

# Find temp gradient
fx, fy = temp_gradient(xx, yy)

# Utilizaremos ahora la función `quiver` de matplotlib para representar los 
# vectores del gradiente de la función

# tip: hacer todos los vectores de módulo unitario y representar la norma del 
      # gradiente con un colormap.
norm = np.sqrt(fx**2 + fy**2)
fx_norm = fx / norm
fy_norm = fy / norm
plt.figure(figsize=(10, 10))
plt.quiver(xx, yy, fx_norm, fy_norm, norm, scale=40, cmap=plt.cm.Spectral)
plt.show()

# Y quizá otra idea útil sería pintar menos flechas. Para eso podemos reducir 
# el número de puntos indexando los arrays, por ejemplo saltando los elementos 
# impares.
plt.figure(figsize=(10, 10))
plt.quiver(xx[::2,::2], yy[::2,::2], fx_norm[::2,::2], fy_norm[::2,::2], norm[::2,::2], scale=30, cmap=plt.cm.Spectral)
plt.show()

##___________________________ Displacement Field ____________________________##
# Aplicaremos ahora un campo de desplazamientos de la forma:
    # $$  \vec u(\rho,\theta)=\frac{\sin(\pi \theta/2)}{30\rho}\vec g_{\rho} $$
    
def desplazamientos(x, y):
    
    u = np.sqrt(x**2 + y**2)
    v = np.arctan2(y, x)
    
    ux = np.sin(np.pi * v / 2) / (30 * u) * np.cos(v)  # componente x de los desplazamientos
    uy = np.sin(np.pi * v / 2) / (30 * u) * np.sin(v)    # componente y de los desplazamientos
    
    return ux, uy

ux, uy = desplazamientos(xx, yy)

plt.figure(figsize=(10, 10))
plt.quiver(xx[::2,::2], yy[::2,::2], ux[::2,::2], uy[::2,::2], scale=0.5, cmap=plt.cm.Spectral)
plt.show()

# Plot the solid before and after the displacement
plt.figure(figsize=(10, 10))

plt.subplot(121)
plt.plot(xx.flatten(), yy.flatten(), 'k.')
plt.gca().set_aspect(1)

plt.subplot(122)
plt.plot(xx.flatten() + 10 * ux.flatten(),
            yy.flatten() + 10 * uy.flatten(), 'k.')
plt.gca().set_aspect(1)
plt.show()

##___________________ Normal Tensions in radial direction ___________________##
# La expresión que proporciona las tensiones, conocidas las deformaciones es:

    # $$ \sigma_{ij}=\lambda \nabla \cdot \vec u \delta_{ij} + 2\mu \epsilon_{ij} $$

# Donde $\lambda$ y $\mu$ son conocidos como los coeficientes de Lamé que dependen 
# de las propiedades elásticas de cada material y $\epsilon_{ij}$ es la parte 
# simétrica del tensor gradiente del campo vectorial $\vec u$.

# Tomando $\lambda =1$ y $\mu =1$, el tensor de deformaciones en forma matricial 
# resulta:
    
    # $$\sigma_{ij}= \begin{bmatrix} \frac{-\sin(\pi \theta/2)}{15\rho^2} & \frac{\pi\cdot\cos(\pi \theta/2)}{60\rho} & 0 \\ \frac{\pi\cdot\cos(\pi \theta/2)}{60\rho} & \frac{\sin(\pi \theta/2)}{15\rho^2} & 0 \\ 0 & 0 & 0 \end{bmatrix}$$

# Que da lugar a una tensiones normales en la dirección radial:
    
    # $$ \vec g_{\rho} \cdot \sigma \cdot \vec g_\rho\ $$

def tensiones_normales(x, y):
    u = np.sqrt(x**2 + y**2)
    v = np.arctan2(y, x)
    
    tens = - np.sin(np.pi * v / 2) / (15 * u**2)
    
    return tens

ff = tensiones_normales(xx, yy)

plt.figure(figsize=(6, 6))
plt.contourf(xx, yy, ff, 50, cmap=plt.cm.Spectral)
plt.colorbar(fraction=0.045)
plt.gca().set_aspect(1)
plt.show()

# ¿Cómo se ajusta el espacio entre gráficas para que no se solapen los textos? 
# Buscamos en Google "plt.subplot adjust" en el primer resultado tenemos la 
# respuesta http://stackoverflow.com/a/9827848