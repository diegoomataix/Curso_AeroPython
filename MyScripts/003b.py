import glob
import numpy as np
from matplotlib import pyplot as plt

print(glob.glob('*.ipynb'))

glob.glob('../data/swc//*.csv')

def analyze(filename):
    data = np.loadtxt(fname=filename, delimiter=',')
    plt.plot(data.mean(axis=0))   
    plt.show()
    
filenames = glob.glob('../data/swc/*.csv')
filenames = filenames[0:8]
for f in filenames:
    print(f)
    analyze(f)