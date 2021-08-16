###_________ Introduction to automatic learning with scikit-learn __________###

# En los últimos tiempos habrás oído hablar de _machine learning_, _deep learning_, 
# _reinforcement learning_, muchas más cosas que contienen la palabra _learning_ y, 
# por supuesto, _Big Data_. Con los avances en capacidad de cálculo de los últimos 
# años y la popularización de lenguajes de alto nivel, hemos entrado de lleno en 
# la fiebre de hacer que las máquinas aprendan. En esta clase veremos cómo utilizar 
# el paquete `scikit-learn` de Python para poder crear modelos predictivos a partir 
# de nuestros datos de una manera rápida y sencilla.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

# En primer lugar vamos a probar con un ejemplo muy sencillo: ajustar una recta 
# a unos datos. Esto difícilmente se puede llamar _machine learning_, pero nos 
# servirá para ver cómo es la forma de trabajar con `scikit-learn`, cómo se entrenan 
# los modelos y cómo se calculan las predicciones.

# En primer lugar fabricamos unos datos distribuidos a lo largo de una recta con 
# un poco de ruido:

def noisy_line(a=2.0, b=0.8, c=50):
    x = np.random.randn(c)
    y = a * x + b * np.random.randn(c)
    return x, y

x, y = noisy_line()
plt.scatter(x,y)
plt.show()

# El proceso para usar `scikit-learn` es el siguiente:
    # 1. Separar los datos en matriz de características `features` y variable a 
    #    predecir `y`
    # 2. Seleccionar el modelo
    # 3. Elegir los hiperparámetros
    # 4. Ajustar o entrenar el modelo (`model.fit`)
    # 5. Predecir con datos nuevos (`model.predict`)
    
from sklearn.linear_model import LinearRegression
model = LinearRegression(fit_intercept=True)

# Tenemos que hacer este `reshape` para transformar nuestro vector en una matriz 
# de columnas. Rara vez tendremos que repetir este paso, puesto que en la práctica 
# siempre tendremos varias variables.

features = x.reshape(-1, 1)
model.fit(features, y)
y_hat = model.predict(features)

# Para calcular el error, en el módulo `sklearn.metrics` tenemos varias funciones útiles:
from sklearn import metrics
abs_error = metrics.mean_absolute_error(y, y_hat)

# Predict with new data
x_new = np.linspace(x.min(), x.max(), 10)
y_pred = model.predict(x_new.reshape(-1, 1))

plt.scatter(x, y)
plt.plot(x_new, y_pred, 'k--')
plt.scatter(x_new, y_pred, marker='x', lw=3, zorder=10)
plt.fill_between(x_new, y_pred + abs_error, y_pred - abs_error, color="C0", alpha=0.3)
plt.show()

##______________ Quick Overview ______________##
# En aprendizaje automático tenemos dos tipos de problemas:
  # * **Aprendizaje supervisado**, cuando tengo datos _etiquetados_, es decir: 
  #     conozco la variable a predecir de un cierto número de observaciones. 
  #     Pasándole esta información al algoritmo, este será capaz de predecir dicha 
  #     variable cuando reciba observaciones nuevas. Dependiendo de la naturaleza 
  #     de la variable a predecir, tendremos a su vez:
     # - **Regresión**, si es continua (como el caso anterior), o
     # - **Clasificación**, si es discreta o categórica (sí/no, color de ojos, etc)
  # * **Aprendizaje no supervisado**, cuando no tenemos datos _etiquetados_ y por 
  # tanto no tengo ninguna información _a priori_. En este caso usaremos los 
  # algoritmos para descubrir patrones en los datos y agruparlos, pero tendremos 
  # que manualmente inspeccionar el resultado después y ver qué sentido podemos 
  # darle a esos grupos.

# En función de la naturaleza de nuestro problema, `scikit-learn` proporciona una 
# gran variedad de algoritmos que podemos elegir.

##______________ Classification ______________##
from sklearn.datasets import load_digits

digits = load_digits()
print(digits["DESCR"])

# Ya tenemos los datos separados en matriz de características y vector de predicción. 
# En este caso, tendré 64 = 8x8 características (un valor numérico por cada pixel 
# de la imagen) y mi variable a predecir será el número en sí.

features, labels = digits.data, digits.target

# Para visualizar estas imágenes tendremos que hacer un `.reshape`:

num_ = features[42]
label_ = labels[42]
num_.reshape(8, 8).astype(int)

plt.figure(figsize=(2, 2))
plt.imshow(num_.reshape(8, 8), cmap=plt.cm.gray_r)
plt.show()

# Ten en cuenta que nosotros sabemos qué número es cada imagen porque somos humanos 
# y podemos leerlas. El ordenador lo sabe porque están etiquetadas, pero ¿qué pasa 
# si viene una imagen nueva? Para eso tendremos que construir un modelo de 
# clasificación.

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(features, labels)

labels_hat = model.predict(features)
accuracy = metrics.accuracy_score(labels, labels_hat)

# ¡Parece que hemos acertado prácticamente todas! Más tarde volveremos sobre este 
# porcentaje de éxito, que bien podría ser engañoso. De momento, representemos 
# otra medida de éxito que es la matriz de confusión:
    
confusion_mat = metrics.confusion_matrix(labels, labels_hat)
plt.imshow(confusion_mat, cmap=plt.cm.Blues)
plt.show()

##__________ Clustering  __________##
# Una vez que hemos visto los dos tipos de problemas supervisados, vamos a ver 
# cómo se trabajan los problemas no supervisados. En primer lugar vamos a fabricar 
# dos nubes de puntos usando la función `make_blobs`:
    
from sklearn.datasets import make_blobs

features, labels = make_blobs(centers=[[6, 0], [2, -1]], random_state=0)

plt.scatter(features[:, 0], features[:, 1], c=labels, cmap = plt.cm.Spectral)
plt.show()

# Hemos creado dos grupos y algunos puntos se solapan, pero ¿qué pasaría si no 
# tuviésemos esta información visual? Vamos a emplear un modelo de clustering 
# para agrupar los datos:
from sklearn.cluster import KMeans
model = KMeans()
# por defecto tenemos 8 clusters. Veamos qué ocurre: #can change with n_clusters=2
model.fit(features)
centroids = model.cluster_centers_
labels_pred = model.predict(features)

xmin, xmax = features[:, 0].min(), features[:, 0].max()
ymin, ymax = features[:, 1].min(), features[:, 1].max()

# Y ahora preparamos el código para representar todas las regiones:
xx, yy = np.meshgrid(
    np.linspace(xmin, xmax),
    np.linspace(ymin, ymax)
)

mesh = np.c_[xx.ravel(), yy.ravel()]
Z = model.predict(mesh)

plt.pcolormesh(xx, yy, Z.reshape(xx.shape))
plt.scatter(features[:, 0], features[:, 1], marker='x', color='k')#c=labels_pred)
plt.scatter(centroids[:, 0], centroids[:, 1], marker='+', color='r', lw=2)
plt.show()

##______________ Dimensionality Reduction ______________##
# Vamos a rescatar nuestro dataset de los dígitos y tratar de visualizarlo en 
# dos dimensiones, lo que se conoce como _reducción de dimensionalidad_.

from sklearn.manifold import Isomap

model = Isomap(n_components=2)
model.fit(digits.data)

# Y ahora proyectamos los datos usando .transform:
digits_proj = model.transform(digits.data)

plt.scatter(digits_proj[:, 0], digits_proj[:, 1],
            c=digits.target, cmap=plt.cm.Spectral, alpha=0.5)
plt.colorbar()
plt.gca(aspect=1)
plt.show()

##______________ Exercise ______________##
# 1. Visualiza el dataset de las flores (`load_iris`) utilizando las funciones 
#    que tienes más abajo. ¿Hay alguna forma clara de separar las tres especies
#    de flores?
# 2. Separa el dataset en matriz de características `features` y vector de 
#    etiquetas `labels`. Conviértelos a arrays de NumPy usando `.as_matrix()`.
# 3. Reduce la dimensionalidad del dataset a 2 usando `sklearn.manifold.Isomap` 
#    o `sklearn.decomposition.PCA` y usa un algoritmo de clustering con 3 clusters. 
#    ¿Se parecen los clusters que aparecen a los grupos originales?
# 4. Predice el tipo de flor usando un algoritmo de clasificación. Visualiza la 
#    matriz de confusión. ¿Cuál es el porcentaje de aciertos del algoritmo? ¿Es 
#    más certero en algún tipo de flor en concreto? ¿Concuerda esto con lo que 
#    pensaste en el apartado 1?

import pandas as pd

def load_iris_df():
    from sklearn.datasets import load_iris

    iris = load_iris()
    features, labels = iris.data, iris.target

    df = pd.DataFrame(features, columns=iris.feature_names)
    df["species"] = pd.Categorical.from_codes(iris.target, categories=iris.target_names)

    #df = df.replace({'species': {0: iris.target_names[0], 1: iris.target_names[1], 2: iris.target_names[2]}})

    return df

iris_df = load_iris_df()

from pandas.plotting import scatter_matrix
_ = scatter_matrix(iris_df, c=iris_df["species"].cat.codes, figsize=(10, 10))

