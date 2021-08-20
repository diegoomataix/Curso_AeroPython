## Widgets ##
import numpy as np
import matplotlib.pyplot as plt

### Exercise ###
# Same as exercise 1 in 020-matplotlib:
def frecuencias(f1=10.0, f2=100.0):
    max_time = 0.5
    times = np.linspace(0, max_time, 1000)
    signal = np.sin(2 * np.pi * f1 * times) + np.sin(2 * np.pi * f2 * times)
    with plt.style.context("ggplot"):
        plt.plot(signal, label="Señal")
        plt.xlabel("Tiempo ($t$)")
        plt.title("Dos frecuencias")
        plt.legend()

# frecuencias()

from ipywidgets import interact # Only works as Jupyter notebook
interact(frecuencias, f1=(10.0,200.0), f2=(10.0,200.0))