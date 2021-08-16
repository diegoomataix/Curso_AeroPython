###_______________________________ Pandas __________________________________### 
# pandas es una biblioteca de análisis de datos en Python que nos provee de las 
# estructuras de datos y herramientas para realizar análisis de manera rápida. 
# Se articula sobre la biblioteca NumPy y nos permite enfrentarnos a situaciones 
# en las que tenemos que manejar datos reales que requieren seguir un proceso de 
# carga, limpieza, filtrado, reduccióń y análisis.
import pandas as pd
import matplotlib.pyplot as plt

##___________________ Loading and Exploring Data ___________________##
# Tratamos de cargarlo en pandas
data = pd.read_csv("../data/tabernas_meteo_data.txt").head(5)

# Tenemos que hacer los siguientes cambios:
    # * Separar los campos por un número arbitrario de espacios en blanco.
    # * Saltar las primeras líneas.
    # * Dar nombres nuevos a las columnas.
    # * Descartar la columna del día del año (podemos calcularla luego).
    # * Parsear las fechas en el formato correcto.

data = pd.read_csv(
    "../data/tabernas_meteo_data.txt",
    delim_whitespace=True,    # delimitado por espacios en blanco
    usecols=(0, 2, 3, 4, 5),  # columnas que queremos usar
    skiprows=2,  # saltar las dos primeras líneas
    names=['DATE', 'TMAX', 'TMIN', 'TMED', 'PRECIP'],
    parse_dates=['DATE'],
#     date_parser=lambda x: pd.datetime.strptime(x, '%d-%m-%y'),  # Parseo manual
    dayfirst=True,      # ¡Importante
    index_col=["DATE"]  # Si queremos indexar por fechas
)

# Ordenando de más antigua a más moderna
data.sort_index(inplace=True)

# Mostrando sólo las primeras o las últimas líneas
print(data.head())

# Comprobamos los tipos de datos de la columnas
print(data.dtypes)

# Las fechas también se pueden parsear de manera manual con el argumento:
    # date_parser=lambda x: pd.datetime.strptime(x, '%d-%m-%y'),  # Parseo manual
# Para acordarnos de cómo parsear las fechas: http://strftime.org/ !!

# Pedimos info general del dataset
print(data.info())

# Descripción estadística
print(data.describe())

# Una vez convertido en un objeto fecha se pueden obtener cosas como:
print(data.index.dayofweek)

##___________________ Accessing the data ___________________##
# Tenemos dos formas de acceder a las columnas: por nombre o por atributo (si 
# no contienen espacios ni caracteres especiales).

# Accediendo como clave
print(data['TMAX'].head())

# Accediendo como atributo
print(data.TMIN.head())

# Accediendo a varias columnas a la vez
print(data[['TMAX', 'TMIN']].head())

# Modificando valores de columnas
print(data[['TMAX', 'TMIN']] / 10)

# Aplicando una función a una columna entera (ej. media numpy)
import numpy as np
print(np.mean(data.TMAX))

# Calculando la media con pandas
print(data.TMAX.mean())

# Para acceder a las filas tenemos dos métodos: `.loc` (basado en etiquetas), 
# `.iloc` (basado en posiciones enteras) y `.ix` (que combina ambos). #.ix not working now

# Accediendo a una fila por índice
print(data.iloc[1])

# Accediendo a una fila por etiqueta
print(data.loc["2016-09-02"])

# Puedo incluso hacer secciones basadas en fechas:
print(data.loc["2016-12-01":]) # Note the ':'

# También puedo indexar utilizando arrays de valores booleanos, por ejemplo 
# procedentes de la comprobación de una condición:
print(data.loc[data.TMIN.isnull()])

# Podemos agrupar nuestros datos utilizando groupby:
    
# Agruparemos por año y día: creemos dos columnas nuevas
data['year'] = data.index.year
data['month'] = data.index.month

# Creamos la agrupación
monthly = data.groupby(by=['year', 'month'])

# Podemos ver los grupos que se han creado
print(monthly.groups.keys())

# Accedemos a un grupo
print(monthly.get_group((2016,3)).head())

# O hacemos una agregación de los datos:
monthly_mean = monthly.mean()
print(monthly_mean.head(24))

# Y podemos reorganizar los datos utilizando pivot tables:
# Dejar los años como índices y ver la media mensual en cada columna
print(monthly_mean.reset_index().pivot(index='year', columns='month'))

# Por último, pandas proporciona métodos para calcular magnitudes como medias 
# móviles usando el método `rolling`:
    
# Calcular la media de la columna TMAX
print(monthly.TMAX.mean().head(15))

# Media trimensual centrada
print(monthly_mean.TMAX.rolling(3, center=True).mean().head(15))

##___________________ Plotting the data ___________________##

#__ lines __#
# Pintar la temperatura máx, min, med
data.plot(y=["TMAX", "TMIN", "TMED"])
plt.title('Temperaturas')
plt.show()

#__ boxes __#
data.loc[:, 'TMAX':'PRECIP'].plot.box()
plt.show()

# Pintando la temperatura máxima de las máximas, mínima de las mínimas, media
# de las medias para cada día del año de los años disponnibles
group_daily = data.groupby(['month', data.index.day])

daily_agg = group_daily.agg({'TMED': 'mean', 'TMAX': 'max', 'TMIN': 'min', 'PRECIP': 'mean'})
print(daily_agg.head())

daily_agg.plot(y=['TMED', 'TMAX', 'TMIN'])
plt.show()

#__ special visualization __#

# scatter_matrix #
from pandas.plotting import scatter_matrix
axes = scatter_matrix(data.loc[:, "TMAX":"TMED"])


