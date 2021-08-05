import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt

from scipy import special

np.info(special)

x = np.linspace(0,20,100)
for ii in range(5):
    plt.plot(x, special.jn(ii, x))
plt.grid(True)
