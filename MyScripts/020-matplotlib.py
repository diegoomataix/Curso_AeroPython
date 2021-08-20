import numpy as np
import matplotlib.pyplot as plt # Documentación: http://matplotlib.org/gallery.html#pylab_examples

## Interfaz Pyplot ##
# La interfaz pyplot proporciona una serie de funciones que operan sobre un estado global 
# - es decir, nosotros no especificamos sobre qué gráfica o ejes estamos actuando. 
# Es una forma rápida y cómoda de crear gráficas pero perdemos parte del control.

## Función plot ##
# El paquete pyplot se suele importar bajo el alias plt, de modo que todas las funciones 
# se acceden a través de plt.<funcion>. La función más básica es la función plot:
    
plt.plot([0.0, 0.1, 0.2, 0.7, 0.9], [1, -2, 3, 4, 1])
plt.show()

# Para representar una función:
def f(x):
    return np.exp(-x ** 2)

x = np.linspace(-1, 3, 100)

plt.plot(x, f(x), label="Función f(x)")
plt.xlabel("Eje $x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.title("Función $f(x)$")
plt.show()

## Note: ##
# Con diversas llamadas a funciones dentro de plt. se actualiza el gráfico actual. 
# Esa es la forma de trabajar con la interfaz pyplot.
# Podemos añadir etiquetas, y escribir 𝐿𝐴𝑇𝐸𝑋
# en ellas. Tan solo hay que encerrarlo entre signos de dólar $$.
# Añadiendo como argumento label podemos definir una leyenda

plt.plot(x, f(x), 'ro')
plt.plot(x, 1 - f(x), 'g--')
plt.show()

# same as:
plt.plot(x, f(x), color='red', linestyle='', marker='o')
plt.plot(x, 1 - f(x), c='g', ls='--')
plt.show()

## Styles ##
# Desde matplotlib 1.4 se puede manipular fácilmente la apariencia de la gráfica usando estilos. 
# Para ver qué estilos hay disponibles, escribiríamos plt.style.available.

# No hay muchos pero podemos crear los nuestros. Para activar uno de ellos, usamos plt.style.use. 
# ¡Aquí va el que uso yo! https://gist.github.com/Juanlu001/edb2bf7b583e7d56468a

# Para emplear un estilo solo a una porción del código, creamos un bloque 
# with plt.style.context("STYLE")

with plt.style.context('ggplot'):
    plt.plot(x, f(x))
    plt.plot(x, 1 - f(x))
    plt.show()
    
## Otros tipo de gráficas ##
## Scatter plot ##
N = 100
x = np.random.randn(N)
y = np.random.randn(N)

s = np.abs(50 + 50 * np.random.randn(N))
c = np.random.randn(N)
# Con s y c podemos modificar el tamaño y el color respectivamente. Para el color, 
# a cada valor numérico se le asigna un color a través de un mapa de colores; ese mapa 
# se puede cambiar con el argumento cmap. Esa correspondencia se puede visualizar
# llamando a la función colorbar.
plt.scatter(x, y, s=s, c=c, cmap=plt.cm.Blues)
plt.colorbar()
plt.show()

plt.scatter(x, y, s=s, c=c, cmap=plt.cm.Oranges)
plt.colorbar()
plt.show()
## List of colormaps @ http://scipy-lectures.github.io/intro/matplotlib/matplotlib.html#colormaps

## Contour plot ##
def f(x, y):
    return x ** 2 - y ** 2

x = np.linspace(-2, 2)
y = np.linspace(-2, 2)
xx, yy = np.meshgrid(x, y)
zz = f(xx, yy)

plt.contour(xx, yy, zz)
plt.colorbar()
plt.show()

# La función contourf es casi idéntica pero rellena el espacio entre niveles. 
# Podemos especificar manualmente estos niveles usando el cuarto argumento:
plt.contourf(xx, yy, zz, np.linspace(-4, 4, 100))
plt.colorbar()
plt.show()

# Para guardar las gráficas en archivos aparte podemos usar la función plt.savefig. 
# matplotlib usará el tipo de archivo adecuado según la extensión que especifiquemos. 
# Veremos esto con más detalle cuando hablemos de la interfaz orientada a objetos.

## Varias figuras / subplot ##
x = np.linspace(-1, 7, 1000)

fig = plt.figure()
plt.subplot(211)
plt.plot(x, np.sin(x))
plt.grid(False)
plt.title("Función seno")

plt.subplot(212)
plt.plot(x, np.cos(x))
plt.grid(False)
plt.title("Función coseno")

fig.tight_layout() # Para que no se solapen
plt.show()
# fig

#### Exercise 1 ####
def frecuencias(f1=10.0, f2=100.0):
    max_time = 0.5
    times = np.linspace(0, max_time, 1000)
    signal = np.sin(2 * np.pi * f1 * times) + np.sin(2 * np.pi * f2 * times)
    with plt.style.context("ggplot"):
        plt.plot(signal, label="Señal")
        plt.xlabel("Tiempo ($t$)")
        plt.title("Dos frecuencias")
        plt.legend()
        plt.show()

# frecuencias()

#### Exercise 2 ####
def g(x, y):
    return np.cos(x) + np.sin(y)**2
# Necesitamos muchos puntos en la malla, para que cuando se
# crucen las líneas no se vean irregularidades
x = np.linspace(-2, 3, 1000)
y = np.linspace(-2, 3, 1000)

xx, yy = np.meshgrid(x, y)

zz = g(xx, yy)

# Podemos ajustar el tamaño de la figura con figsize
fig = plt.figure(figsize=(6, 6))
plt.show()

# Ajustamos para que tenga 13 niveles y que use el colormap Spectral
# Tenemos que asignar la salida a la variable cs para luego crear el colorbar
cs = plt.contourf(xx, yy, zz, np.linspace(-1, 2, 13), cmap=plt.cm.Spectral)

# Creamos la barra de colores
plt.colorbar()

# Con `colors='k'` dibujamos todas las líneas negras
# Asignamos la salida a la variable cs2 para crear las etiquetas
cs = plt.contour(xx, yy, zz, np.linspace(-1, 2, 13), colors='k')

# Creamos las etiquetas sobre las líneas
plt.clabel(cs)

# Ponemos las etiquetas de los ejes
plt.xlabel("Eje x")
plt.ylabel("Eje y")
plt.title(r"Función $g(x, y) = \cos{x} + \sin^2{y}$")