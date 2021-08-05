##### Estadística con SciPy #####
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt

### scipy.stats ###
# Importar el módulo entero
import scipy.stats as st

### Functions ###
# Carguemos unos datos, por ejemplo unas notas de la carrera, y veamos cómo 
# podemos aprovechar las funciones de scipy.stats.
datos = np.loadtxt("../data/notas.csv", skiprows=1) # Leemos el archivo
print(st.describe(datos)) # Descripción rápida de los datos
# st.histogram(datos, numbins=10, defaultlimits=(0,10)) # Histograma con st (not working on newer SciPy, try with NumPy)
# Pintemos un histograma con plt
# plt.hist(datos, range(0,11,))
# plt.xticks(range(0,11))
# plt.grid(True)

# plt.vlines(5, 0, 100, lw=5, colors='red', alpha=0.8)
# plt.fill_between([0, 5], [100, 100], color='red', alpha=0.5)

# Pintemos un histograma acumulado con plt
# plt.hist(datos, range(0,11), cumulative=True)
# plt.xticks(range(0,11))

# plt.vlines(5, 0, 400, lw=5, colors='red', alpha=0.8)
# plt.fill_between([0, 5], [400, 400], color='red', alpha=0.5)
# plt.grid(True)

# # Percentil
# print(st.percentileofscore(datos, 5))
# # Nota de un percentil
# print(st.scoreatpercentile(datos, 50))

### Distribuciones estadísticas ###
# Parámetros
med = np.nanmean(datos)
des_tip = np.nanstd(datos)

# Distribución normal
dist_normal = st.norm(loc=med, scale=des_tip)
## Note!
    # Función densidad de probabilidad (probability density function) pdf
    # Función de distribución (cumulative distribution function) cdf
# Calculamos la pdf
x = np.linspace(0, 10, 100)
y1 = dist_normal.pdf(x)
# La representamos
# with plt.style.context('seaborn-notebook'):
#     plt.plot(x, y1)
#     plt.grid(True)
# Calculamos la cdf
y2 = dist_normal.cdf(x)
# La representamos
# with plt.style.context('seaborn-notebook'):
#     plt.plot(x, y2)
#     plt.grid(True)

### Tests ###
# Ahora que ya hemos visualizado la distribución de las notas y que sabemos 
# generar distribuciones normales. ¿Por qué no hacemos un test de Kolmogórov-Smirnov?
# Se trata de ver lo bien o lo mal que se ajusta la distribución a una normal 
bars = np.histogram(datos, bins=10)
# bars /= 375

plt.bar(np.arange(0,10), bars, alpha=0.5, width=1)
plt.plot(x, y1, c='black', lw=2)

plt.grid(True)

