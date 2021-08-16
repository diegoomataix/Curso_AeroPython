# fichero que se llama model.txt que contiene datos de medidas de viento: 
# velocidad, orientación, temperatura...

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

model = pd.read_csv(
    "../data/model.txt", delim_whitespace=True, skiprows = 3,
    parse_dates = {'Timestamp': [0, 1]}, index_col = 'Timestamp')

##_______________ Ejercicios _______________##
# Sobre el conjunto de datos `model`:
    # 1. Representar la matriz `scatter` de la velocidad y orientación del viento 
    #    de los primeros mil registros.
    # 2. Misma matriz scatter para los 1000 registros con mayor velocidad, ordenados.
    # 3. Histograma de la velocidad del viento con 36 particiones.
    # 4. Histórico de la velocidad media, con los datos agrupados por años y meses.
    # 5. Tabla de velocidades medias en función del año (filas) y del mes (columnas).
    # 6. Gráfica con los históricos de cada año, agrupados por meses, superpuestos.
    
    ## FIXED ## # AttributeError: module 'pandas' has no attribute 'tools', now no need for tools
    
    ## FIXED ## .ix has been depreciated, use .loc and dataname.index[] for indexing with values 

# 1
pd.plotting.scatter_matrix(model.loc[model.index[:1000], 'M(m/s)':'D(deg)']) 
plt.show()

# 2
pd.plotting.scatter_matrix(
    model.sort_values('M(m/s)', ascending=False).loc[model.index[:1000], 'M(m/s)':'D(deg)'])
plt.show()

# 3
model.loc[:, 'M(m/s)'].plot.hist(bins=np.arange(0, 35))
plt.show()


# 4
model['month'] = model.index.month
model['year'] = model.index.year
av_vel_hist = model.groupby(by = ['year', 'month']).mean().head(24)
model.groupby(by=['year', 'month']).mean().plot(y='M(m/s)', figsize=(15, 5))
plt.show()


# Media móvil de los datos agrupados por mes y año:
monthly = model.groupby(by=['year', 'month']).mean()
monthly['ma'] = monthly.loc[:, 'M(m/s)'].rolling(5, center=True).mean()
monthly.loc[:, ['M(m/s)', 'ma']].plot(figsize=(15, 6))
plt.show()

# 6
monthly.loc[:, 'M(m/s)'].reset_index().pivot(
    index='year', columns='month'
).T.loc['M(m/s)'].plot(
    figsize=(15, 5), legend=False
)
plt.show()

