import numpy as np
import matplotlib.pyplot as plt

###_____ La transformación de Yukovski es: $$\tau=t+\frac{a^{2}}{t}$$ ______###
    # Problem parameters @ notebooks_completos/090-Ejemplos-Yukovski.ipynb
# Los parámetros del problema: #

# Datos para el perfil de Yukovski
# Parámetro de la transformación de Yukovski
a = 1

# Centro de la circunferencia
landa = 0.2     # coordenada x (en valor absoluto)
delta = 0.3     # coordenada y

t0 = a * (-landa + delta * 1j)     # centro: plano complejo

# Valor del radio de la circunferencia
R = a * np.sqrt((1 + landa)**2 + delta**2)

# Ángulo de ataque corriente incidente
alfa_grados = 15
alfa = np.deg2rad(alfa_grados)

#Velocidad de la corriente incidente
U = 1

###__________________ Yukoski profile from a circumfence ___________________###

##_________ Yukoski Transformation Function _________##
# Se trata de definir una función que realice la transformación de Yukovski. 
# Esta función recibirá el parámetro de la transformación, a y el punto del plano
# complejo t. Devolverá el valor tau, punto del plano complejo en el que se transforma t.
def transf_yukovski(a, t):
    """Dado el punto t (complejo) y el parámetro a
    a de la transformación proporciona el punto
    tau (complejo) en el que se transforma t."""
    tau = t + a ** 2 / t
    return tau
#comprobamos que la función está bien programada
#puntos del eje real siguen siendo del eje real
# err_message = "La transformación de Yukovski no devuelve un resultado correcto"
# np.testing.assert_equal(transf_yukovski(1, 1+0j), 2+0j, err_message)

##_________ Circumference _________##
# Ahora queremos transformar la circunferencia de radio $R$ con centro en $t_0$
# usando la función anterior:
    # 1. __Creamos `N` puntos de la circunferencia de modo que en `Xc` estén
    # las coordenadas $x$ y en `Yc` estén las coordenadas $y$ de los puntos que
    # la forman. Controla el número de puntos mediante un parámetro que se llame
    # `N_perfil`.
         #     $$X_c = real(t_0) + R·cos(\theta)$$
         #     $$Y_c = imag(t_0) + R·sin(\theta)$$
    # 2. Una vez hayas obtenido los dos arrays `Xc` e `Yc`, píntalos mediante
    # un `scatter` para comprobar que todo ha ido bien.
    # 3. Pinta también el centro de la circunferencia.

# Número de puntos de la circunferencia que 
# vamos a transformar para obtener el perfil
N_perfil = 100

# Se barre un ángulo de 0 a 2 pi
theta = np.linspace(0, 2*np.pi, N_perfil)

# Se crean las coordenadas del los puntos de la circunferencia
Xc = np.real(t0) + R * np.cos(theta)
Yc = np.imag(t0) + R * np.sin(theta)

# Visualize
plt.figure("Circumference", figsize=(5,5))
plt.title('Circumference', {'fontsize':20})
p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=3) # zorder:Set the zorder for the artist. Artists with lower zorder values are drawn first.
plt.gca().add_patch(p)

plt.ylim(-1.5, 2)
plt.xlim(-2, 1.5)
plt.grid()
plt.show()

##_________ Transform Circumference to Profile _________##
# Ahora estamos en condiciones de transformar estos puntos de la circunferencia 
# (Xc, Yc) en los del perfil (Xp, Yp). Para esto vamos a usar nuestra función 
# transf_yukovski. Recuerda que esta función recibe y da números complejos. 
Puntos_perfil = transf_yukovski(a, Xc+Yc*1j)
Xp, Yp = np.real(Puntos_perfil) , np.imag(Puntos_perfil)

#lo visualizamos
plt.figure('Yukovski Profile', figsize=(10,10))
plt.title('Yukovski Profile', {'fontsize':20})
p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=3)
plt.gca().add_patch(p)
plt.gca().set_aspect(1)

plt.xlim(-3, 3)
plt.ylim(-0.4,1)
plt.grid()
plt.show()

###_____________________ Flow around the cylinder __________________________###
# Para visualizar ahora el flujo alrededor del cilindro recurrimos al __potencial 
# complejo__ de una _corriente uniforme_ que forme un ángulo $\alpha$ con el eje 
# $x$ _en presencia de un cilindro_ (aplicando el teorema del círculo) y se añade 
# un torbellino con la intensidad adecuada para que se cumpla la hipótesis de Kutta 
# en el perfil:
    # f(t)=U_{\infty}\text{·}\left((t-t_{0})\text{·}e^{-i\alpha}+\frac{R^{2}}{t-t_{0}}\
        # text{·}e^{i\alpha}\right)+\frac{i\Gamma}{2\pi}\text{·}ln(t-t_{0})=\Phi+i\Psi
# donde $\Phi$ es el potencial de velocidades y $\Psi$ es la función de corriente.
    # $$\Gamma = 4  \pi  a  U  (\delta + (1+\lambda)  \alpha)$$
# $\Gamma$ es la circulación que hay que añadir al cilindro para que al transformarlo 
# en el perfil se cumpla la condición de Kutta.
# Recordando que la función de corriente toma un valor constante en las líneas 
# de corriente, sabemos que: dibujando $\Psi=cte$ se puede visualizar el flujo.
# __Pintaremos estas lineas de potencial constante utilizando la función `contour()`
# , pero antes tendremos que crear una malla circular. Esto será lo primero que 
# hagamos:__
    # 1. Crea un parámetro `N_R` cuyo valor sea el número de puntos que va a tener 
    # la malla en dirección radial. Desde otro punto de vista, esta parámetro es 
    # el número de círculos concéntricos que forman la malla.
    # 2. Crea dos parámetros `R_min` y `R_max` que representen el radio mínimo 
    # y máximo entre los que se extiende la malla. El radio mínimo debe de ser 
    # el radio del círculo, porque estamos calculando el aire en el exterior del
    # perfil.
    # 4. La dirección tangencial necesita un sólo parámetro `N_T`, que representa 
    # el número de puntos que la malla tendrá en esta dirección. Dicho de otro modo, 
    # cuántos puntos forman los círculos concéntricos de la malla.
    # 3. Crea un array `R_` que vaya desde `R_min` hasta `R_max` y que tenga `N_R` 
    # elementos. De manera análoga, crea el array `T_`, que al representar los 
    # ángulos de los puntos que forman las circunferencias, debe ir de 0 a 2$\pi$, 
    # y tener `N_T` elementos.
    # 4. Para trabajar con la malla, deberemos usar coordenadas cartesianas. 
    # Crea la malla: `XX, YY` van a ser dos matrices de `N_T · N_R` elementos. 
    # Cada elemento de estas matrices se corresponde con un punto de la malla: 
    # la matriz `XX` contiene las coordenadas X de cada punto y la matriz `YY`, 
    # las coordenadas y. 
# La manera de generar estas matrices tiene un poco de truco, porque depende de 
# ambos vectores.
# Para cada elemento, 
    # $x = real(t_0) +  R · cos (T) $ ,  $y = imag(t_0) + R · sin(T)$. 
    
# __Recuerda que:__
# * Los puntos sobre la circunferencia se transforman en el perfil.
# * Los puntos interiores a la circunferencia se transforman en puntos interiores
# al perfil.
# * Los puntos exteriores a la circunferencia se transforman en puntos exteriores
# al perfil. __Los puntos que nos interesan__.

#se crea la malla donde se va pintar la función de corriente
# Dirección radial
N_R = 50   # Número de puntos en la dirección radial
R_min = R
R_max = 10

# Dirección tangencial
N_T = 180   # Número de puntos en la dirección tangencial

R_ = np.linspace(R_min, R_max, N_R)

T_ = np.linspace(0, 2*np.pi , N_T)

# Crear la malla:
XX =  R_ * np.cos(T_).reshape((-1, 1)) + np.real(t0)
YY = R_ * np.sin(T_).reshape((-1, 1)) + np.imag(t0)

#pintamos la malla para verla
plt.figure(figsize=(10,10))
plt.scatter(XX.flatten(), YY.flatten(), marker='.')
plt.show()

# Bueno, lo que queríamos era hacer cosas alrededor de nuestro perfil,
# Esto lo conseguiremos pintando la función Phi en los puntos XX_tau, YY_tau 
# transformados de los XX, YY a través de la función transf_yukovski, recuerda 
# que la transformación que tenemos recibe y da números complejos. Como antes, 
# debes separar parte real e imaginaria. En la siguiente celda calcula y transforma 
# tt (donde debe estar almacenada la malla en forma compleja) para obtener XX_tau, 
# YY_tau.

# Probemos a visualizar como se transforman los puntos de la malla primero.
tt = XX + YY * 1j
tautau = transf_yukovski(a, tt)
XX_tau, YY_tau = np.real(tautau) , np.imag(tautau)
# Comprobamos que los puntos exteriores a la circunferencia se transforman en los puntos exteriores del perfil
#pintamos la malla para verla
plt.figure(figsize=(10,10))
plt.scatter(XX_tau.flatten(), YY_tau.flatten(), marker='.')
plt.show()

##_________ Obtaining the Flow _________##
# 1. Crea una variable `T` que tenga el valor correspondiente a la circulación 
    # $\Gamma$.
# 2. Utilizando el array `tt`, el valor `T` y los parámetros definidos al 
    # principio (`t0, alfa, U...`) crea `f` según la fórmula de arriba (no hace 
    # falta que crees una función).
# 3. Guarda la parte imaginaria de esa función (función de corriente) en una 
    # variable `psi`.

# Circulación que hay que añadir al cilindro para
# que se cumpla la hipótesis de Kutta en el perfil
T = 4 * np.pi * a * U * (delta + (1+landa) * alfa)

# Malla compleja
tt = XX + YY * 1j

# Potencial complejo
f = U * ( (tt - t0) * np.exp(-alfa *1j) + R**2 / (tt - t0) * np.exp(alfa * 1j) )
f += 1j * T / (2* np.pi) * np.log(tt - t0)
    
# Función de corriente
psi = np.imag(f)

# Como la función de corriente toma un valor constante en cada línea de corriente, 
# podemos visualizar el flujo alrededor del cilindro pintando las lineas en las 
# que psi toma un valor constante. Para ello utilizaremos la función contour() 
# en la malla XX, YY. Si no se ve nada prueba a cambiar el número de líneas y 
# los valores máximo y mínimo de la función que se representan.

plt.figure('lineas de corriente', figsize=(10,10))

#ponemos el cilindro encima
plt.figure('flujo cilindro', figsize=(10,10))

plt.contour(XX, YY, psi, np.linspace(-5,5,50)) # colors=['blue', 'blue']
plt.grid()
plt.gca().set_aspect(1)
p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=3)
plt.gca().add_patch(p)
plt.show()

###________________________ Flow around the Profile ________________________###
plt.figure("flujo perfil", figsize=(12,12))

plt.contour(XX_tau, YY_tau, psi, np.linspace(-5, 5, 50)) # , colors=['blue', 'blue']
p = plt.Polygon(list(zip(Xp, Yp)), color="#cccddd", zorder=5)
plt.gca().add_patch(p)

plt.xlim(-8,8)
plt.ylim(-3,3)
plt.grid()
plt.gca().set_aspect(1)
plt.show()

###__________________ Interact ___________________###
##### ONLY WORKS IN JUPYTER NOTEBOOK #####
# Vamos a usar un interact, ¿no?
# Tenemos que crear una función que haga todas las tareas: reciba los argumentos 
# y pinte para llamar a interact con ella. No tenemos más que cortar y pegar.

def transformacion_geometrica(a, landa, delta, N_perfil=100):
    #punto del plano complejo
    t0 = a * (-landa + delta * 1j)
    #valor del radio de la circunferencia
    R = a * np.sqrt((1 + landa)**2 + delta**2)
    #se barre un ángulo de 0 a 2 pi
    theta = np.linspace(0, 2*np.pi, N_perfil)
    #se crean las coordenadas del los puntos
    #de la circunferencia
    Xc = - a * landa + R * np.cos(theta)
    Yc =   a * delta + R * np.sin(theta)
    #se crean las coordenadas del los puntos
    #del perfil
    Puntos_perfil = transf_yukovski(a, Xc+Yc*1j)
    Xp, Yp = np.real(Puntos_perfil) , np.imag(Puntos_perfil)
    
    #Se pintan la cirunferencia y el perfil
    fig, ax = plt.subplots(1,2)
    fig.set_size_inches(15,15)
    p_c = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=1)
    ax[0].add_patch(p_c)
    ax[0].plot(Xc,Yc)
    ax[0].set_aspect(1)
    ax[0].set_xlim(-3, 3)
    ax[0].set_ylim(-2,2)
    ax[0].grid()
    
    p_p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=1)
    ax[1].add_patch(p_p)
    ax[1].plot(Xp,Yp)
    ax[1].set_aspect(1)

    ax[1].set_xlim(-3, 3)
    ax[1].set_ylim(-2,2)
    ax[1].grid()
    plt.show()

# from ipywidgets import interact

# interact(transformacion_geometrica, landa=(-1.,1, 0.01), delta=(-1.,1,0.01), 
             # a=(0,2.,0.1), N_perfil=(4, 200) )

# aeropython: preserve
def flujo_perfil_circunferencia(landa, delta, alfa, U=1,  N_malla = 100):
    N_perfil=N_malla
    a=1
    #punto del plano complejo
    t0 = a * (-landa + delta * 1j)
    #valor del radio de la circunferencia
    R = a * np.sqrt((1 + landa)**2 + delta**2)

    #se barre un ángulo de 0 a 2 pi
    theta = np.linspace(0, 2*np.pi, N_perfil)
    #se crean las coordenadas del los puntos
    #de la circunferencia
    Xc = - a * landa + R * np.cos(theta)
    Yc =   a * delta + R * np.sin(theta)
    
    #se crean las coordenadas del los puntos
    #del perfil
    Puntos_perfil = transf_yukovski(a, Xc+Yc*1j)
    Xp, Yp = np.real(Puntos_perfil) , np.imag(Puntos_perfil)
    
    #se crea la malla donde se va pintar la función de corriente

    # Dirección radial
    N_R = N_malla//2   # Número de puntos en la dirección radial
    R_min = R
    R_max = 10

    # Dirección tangencial
    N_T = N_malla   # Número de puntos en la dirección tangencial

    R_ = np.linspace(R_min, R_max, N_R)
    T_ = np.linspace(0, 2*np.pi , N_T)

    # El menos en la XX  es para que el borde de ataque del perfil esté en la izquierda
    XX = - (R_ * np.cos(T_).reshape((-1, 1)) - np.real(t0))
    YY = R_ * np.sin(T_).reshape((-1, 1)) + np.imag(t0)
    
    tt = XX + YY * 1j
    
    alfa = np.deg2rad(alfa)
    # Circulación que hay que añadir al cilindro para
    # que se cumpla la hipótesis de Kutta en el perfil
    T = 4 * np.pi * a * U * (delta + (1+landa) * alfa)
    #Potencial complejo
    f = U * ( (tt - t0) * np.exp(-alfa *1j) + R**2 / (tt - t0) * np.exp(alfa * 1j) )
    f += 1j * T / (2* np.pi) * np.log(tt - t0)
    #Función de corriente
    psi = np.imag(f)   

    Puntos_plano_tau = transf_yukovski(a, tt)
    XX_tau, YY_tau = np.real(Puntos_plano_tau) , np.imag(Puntos_plano_tau)
                
    #Se pinta
    fig, ax = plt.subplots(1,2)
    #lineas de corriente
    fig.set_size_inches(15,15)
    
    ax[0].contour(XX, YY, psi, np.linspace(-10,10,50), colors = ['blue', 'blue'])
    ax[0].grid()
    ax[0].set_aspect(1)
    p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=10)
    ax[0].add_patch(p)
    ax[0].set_xlim(-5, 5)
    ax[0].set_ylim(-2,2)
    
    ax[1].contour(XX_tau, YY_tau, psi, np.linspace(-10,10,50), colors = ['blue', 'blue'])
    ax[1].grid()
    ax[1].set_aspect(1)
    p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=10)
    ax[1].add_patch(p)
    ax[1].set_xlim(-5, 5)
    ax[1].set_ylim(-2,2)
    plt.show()
    
# p = interact(flujo_perfil_circunferencia, landa=(0.,1), delta=(0.,1), alfa=(0, 30), U=(0,10), N_malla = (10,150))

###_____________________________ MORE PLOTS ________________________________###
# podemos fácilmente pintar la velocidad y la presión del aire alrededor del perfil.

#Velocidad conjugada
dfdt = U * ( 1 * np.exp(-alfa * 1j) - R**2 / (tt - t0)**2 * np.exp(alfa * 1j) )
dfdt += 1j * T / (2*np.pi) * 1 / (tt - t0)
#coeficiente de presion
cp = 1 - np.abs(dfdt)**2 / U**2
cmap = plt.cm.RdBu

#Se pinta
fig, ax = plt.subplots(1,3)
#lineas de corriente
fig.set_size_inches(15,15)
ax[0].contour(XX, YY, psi, np.linspace(-10,10,50), colors = ['blue', 'blue'])
ax[0].grid()
ax[0].set_aspect(1)
p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=10)
ax[0].add_patch(p)
#Campo de velocidades
ax[1].contourf(XX, YY, np.abs(dfdt), 200, cmap=cmap)
p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=10)
ax[1].set_title('campo de velocidades')
ax[1].add_patch(p)
ax[1].set_aspect(1)
ax[1].grid()
#campo de presiones
ax[2].contourf(XX, YY, cp, 200, cmap=cmap)
p = plt.Polygon(list(zip(Xc, Yc)), color="#cccccc", zorder=10)
ax[2].set_title('coeficiente de presión')
ax[2].add_patch(p)
ax[2].set_aspect(1)
ax[2].grid()
plt.show()

# Se pinta
fig, ax = plt.subplots(1,3)
#lineas de corriente
fig.set_size_inches(15,15)
ax[0].contour(XX_tau, YY_tau, psi, np.linspace(-10,10,50), colors = ['blue', 'blue'])
ax[0].grid()
ax[0].set_aspect(1)
p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=10)
ax[0].add_patch(p)
#Campo de velocidades
ax[1].contourf(XX_tau, YY_tau, np.abs(dfdt), 200, cmap=cmap)
p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=10)
ax[1].set_title('campo de velocidades')
ax[1].add_patch(p)
ax[1].set_aspect(1)
ax[1].grid()
#campo de presiones
ax[2].contourf(XX_tau, YY_tau, cp, 200, cmap=cmap)
p = plt.Polygon(list(zip(Xp, Yp)), color="#cccccc", zorder=10)
ax[2].set_title('coeficiente de presión')
ax[2].add_patch(p)
ax[2].set_aspect(1)
ax[2].grid()
plt.show()