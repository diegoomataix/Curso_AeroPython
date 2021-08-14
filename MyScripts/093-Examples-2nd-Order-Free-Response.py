###________________________ 2nd-Order-Free-Response ________________________###

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 22})

##__________ Functions for dumping characteristic cases __________##
def undumped(wn, x0, x_dot0, t):
    return x0 * np.cos(wn * t) + x_dot0 / wn * np.sin(wn * t)

def underdumped(xi, wn, x0, x_dot0, t):
    
    wd = wn * np.sqrt(1 - xi**2)
    
    x = (
        np.exp(-xi*wn*t) *
        (
            x0 * np.cos(wd * t) +
            (xi*wn*x0 + x_dot0) / wd * np.sin(wd * t)
        )
    )
    return x

def critically_dumped(wn, x0, x_dot0, t):
    return np.exp(-wn*t) * (x0 * (1 + wn * t) + x_dot0 * t)

def overdumped(xi, wn, x0, x_dot0, t):
    a = xi * wn + wn * np.sqrt(xi**2 - 1)
    b = xi * wn - wn * np.sqrt(xi**2 - 1)
    
    x = (
        (a * x0 + x_dot0) / (a - b) * np.exp(-b*t) - 
        (b * x0 + x_dot0) / (a - b) * np.exp(-a*t)
        )    
    return x

##__________ 2nd order free response __________##
def plot_2order_free_resp(xi, wn, x0, x_dot0):
    
    t = np.linspace(0, 10, 1000)
    
    # Calculate selected     
    if np.isclose(xi, 0):
        x = undumped(wn, x0, x_dot0, t)
    elif np.isclose(xi, 1):
        x = critically_dumped(wn, x0, x_dot0, t)
    elif 0 < xi < 1:
        x = underdumped(xi, wn, x0, x_dot0, t)
    else:
        x = overdumped(xi, wn, x0, x_dot0, t)
    
    # Plot selected
    plt.figure(figsize=(15, 8))
    plt.plot(t, x, ls='-', lw=2, c='#b30000', label=f"$\\xi={xi:.2f}$")
        
    # Critical dumping     
    x = critically_dumped(wn, x0, x_dot0, t)
    plt.plot(t, x, ls='--', lw=4, alpha=0.7, c='#02818a', label="$\\xi=1.00$")
    
    # No dumping     
    x = undumped(wn, x0, x_dot0, t)
    
    # Formatting
    plt.title("$\omega_n$ = {}, $x_0$ = {}, $\\dotx_0$ = {}".format(wn, x0, x_dot0))
    plt.plot(t, x, ls='-', lw=4, alpha=0.5, c='#0570b0', label="$\\xi=0.00$")
    
    plt.ylim(-1, 1)
    plt.xlim(0,10)
    plt.grid()
    plt.xlabel('t')
    plt.ylabel('x')
    plt.legend(loc='upper right')

for xii in [1.5, 1.85, 2.5]:
# for xii in [0.00, 1.00, 2.50]:
    for wnn in [1, 3, 5]:
        for x00 in [-1, -0.5, 0]:
            for x_dot00 in [1.5, 3.6, 4.5]:
                plot_2order_free_resp(xii, wnn, x00, x_dot00)
                

