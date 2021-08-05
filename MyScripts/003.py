import matplotlib.pyplot as plt
import numpy as np


def analyze(file):
    """does things"""
    data = np.loadtxt(file, delimiter=',')

    plt.plot(data.mean(axis=1))
    plt.show()
    
    return data.max(), data.mean(), data.min()


analyze("../data/swc/inflammation-01.csv")



