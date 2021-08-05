import matplotlib.pyplot as plt
import numpy as np

# Almacenando los datos
data = np.loadtxt(fname='../data/swc/inflammation-01.csv', delimiter=',')

print(data)

# plt.matshow(data)
# plt.matshow(data[:3,:])

plt.plot(data.mean(axis=0))

plt.plot(data.max(axis=0))
plt.plot(data.min(axis=0))