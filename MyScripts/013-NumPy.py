import numpy as np

### Ejercicio ###
# Pintar un tablero de ajedrez usando la función plt.matshow

checkboard = np.zeros([8, 8], dtype=int)

checkboard[0::2, 1::2] = 1
checkboard[1::2, 0::2] = 1

# matplotlib inline
import matplotlib.pyplot as plt

plt.matshow(checkboard, cmap=plt.cm.gray_r)