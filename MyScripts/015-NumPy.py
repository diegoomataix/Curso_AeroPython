### NumPy: Entrada/Salida (I/O) ###

# Para el caso de la lectura se usa la función np.loadtxt
# Primero, importamos las librerías que vamos a usar: Numpy y Matplotlib. 
# También usaremos plt.ion() para activar el modo interactivo de matplotlib
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

## Cargando los datos ##
# Usaremos la función loadtxt para cargar los datos en un array. Usaremos los 
# argumentos opcionales skiprows, delimiter y usecols para captar los datos que queremos

# loading the data:
# ./data/barrio_del_pilar-20160322.csv
data1 = np.loadtxt('../data/barrio_del_pilar-20160322.csv', skiprows=3, delimiter=';', usecols=(2,3,4))
data1[:10,:]

## Valores inexistentes: ##
# El archivo que contiene los datos de 2015 tiene algunos agujeros por errores de medida. 
# Como alternativa a loadtxt, podremos usar la función genfromtxt, teniendo cuidado 
# de que el ella el argumento opcional de saltar líneas pasa a llamarse skip_header.
#Loading the data 2:
#../data/barrio_del_pilar-20151222.csv
data2 = np.genfromtxt('../data/barrio_del_pilar-20151222.csv', skip_header=3, delimiter=';', usecols=(2,3,4))
data2[:10,:]

# Podemos comprobar como afecta la existencia de estos valores a algunas funciones de Numpy, 
# como np.mean. A veces es posible esquivar estos problemas con otras funciones como np.nanmean
print(np.mean(data2, axis=0))
print(np.nanmean(data2, axis=0))

data_dif = data1 - data2
data_dif[:10,:]

## Guardar los datos nuevos ##
# Supongamos que ahora queremos guardar nuestra tabla de datos en un archivo txt, 
# para poder cargarlo ya modificado más adelante. Una manera fácil de hacerlo sería 
# con otra función de NumPy: np.savetxt. Lo usaremos con los argumentos opcionales 
# fmt='%9.3f', newline = '\r\n' para obtener un fichero bonito que podamos entender de un vistazo.
np.savetxt('diferencia_interanual.txt', data_dif, fmt='%9.3f', newline = '\r\n')

## Pintando los datos: ##
# # Valores máximos obtenidos de: http://www.mambiente.munimadrid.es/opencms/export/sites/default/calaire/Anexos/valores_limite_1.pdf
# plt.plot(data1[:, 1], label='2016')
# plt.plot(data2[:, 1], label='2015')

# plt.legend()

# plt.hlines(200, 0, 200, linestyles='--')
# plt.hlines(40, 0, 200, linestyles='--')
# plt.ylim(0, 220)

# http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.convolve.html
def moving_average(x, N=8):
    return np.convolve(x, np.ones(N)/N, mode='same')

# plt.plot(moving_average(data1[:, 0]), label='2016')
# plt.plot(moving_average(data2[:, 0]), label='2015')

# plt.hlines(10, 0, 250, linestyles='--')
# plt.ylim(0, 11)

# plt.legend()

# plt.plot(moving_average(data1[:, 2]), label='2016')
# #plt.plot(data1[:, 2])

# plt.plot(moving_average(data2[:, 2]), label='2015')
# #plt.plot(data2[:, 2])

# plt.hlines(180, 0, 250, linestyles='--')
# plt.ylim(0, 190)

# plt.legend()

## ¿Cómo leeríamos un archivo sin usar NumPy? ##
# data_file = '../data/barrio_del_pilar-20151222.csv'
# data = []

# with open(data_file) as f:
#     # Saltamos las tres primeras líneas
#     for ii in range(3):
#         f.readline()
    
#     for line in f:
#         line_string = line
#         line_list = line.split(';')
        
#         date = line_list[0]
#         hour = line_list[1]
        
#         components_data = []
#         for c in line_list[2:]:
#             if '-' not in c:
#                 components_data.append(float(c))
#             else:
#                 components_data.append(np.nan)
#         data.append(components_data)
        
# print(np.array(data))

