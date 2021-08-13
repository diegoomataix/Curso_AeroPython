###__________________________ SymPy - Mechanics ____________________________###

##_________ Reference System _________##
# El objeto primordial que vamos a manejar van a ser los sistemas de referencia. 
# Podremos definir relaciones geométricas entre ellos y de esta forma las transformaciones 
# de vectores entre un sistema y otro serán triviales.

# La manera usual de empezar a trabajar con SymPy es importar la función init_session:
from sympy import init_session, Symbol, symbols, pi, I, E, cos, sin, exp, tan, simplify, expand, factor, collect, apart, cancel, expand_trig, diff, Derivative, Function, integrate, limit, series, Eq, solve, dsolve, Matrix, N
# from sympy import init_session
init_session(use_latex=True)

# Todo lo que necesitamos está en sympy.physics.mechanics, incluyendo la clase ReferenceFrame. 
# Nada más crear un sistema de referencia podemos acceder a sus versores unitarios: x, y y z.

from sympy.physics.mechanics import ReferenceFrame 

# A = ReferenceFrame("A")
# print(A.x)

# Y para definir vectores solo tenemos que multiplicar cada componente por su versor:
# print(2 * A.x - 1 * A.y)

# De ahora en adelante, para trabajar como si nos enfrentáramos a un problema de 
# la escuela, vamos a hacer dos cosas:
    # [-] Definir un sistema inercial 1 del que partir, para así poder referir todos 
    # los demás sistemas a él.
    # [-] Que los versores de ese sistema sean 𝑖,𝑗,𝑘
    
# A = ReferenceFrame("1", latexs=['\mathbf{i}', '\mathbf{j}', '\mathbf{k}'])
# print(A.x + A.y + A.z)

# Y para no tener que hacerlo siempre, un pequeño truco de magia:
# Definimos nuestra propia clase para que los versores sean IJK
#------------------------------------------------------------------------------
class IJKReferenceFrame(ReferenceFrame):
    def __init__(self, name):
        super().__init__(name, latexs=['\mathbf{%s}_{%s}' % (idx, name) for idx in ("i", "j", "k")])
        self.i = self.x
        self.j = self.y
        self.k = self.z
#------------------------------------------------------------------------------
A = IJKReferenceFrame("1")
print(A.x + A.y + A.z)

##_________ Vectorial Algebra _________##
# Nuestros vectores funcionan también con símbolos, y podemos realizar las operaciones 
# de producto escalar y producto vectorial con ellos.
R, V = symbols('R, V', positive=True)
r1 = R * (A.x + A.y + A.z)
v1 = V * (A.x - 2 * A.z)

from sympy.physics.mechanics import dot, cross

print(r1.dot(v1))
print(dot(r1, v1))
print(r1 & v1)

print(r1.cross(v1))
print(cross(r1, v1))
print(r1 ^ v1)

# Podemos hallar también la norma de los vectores con su método magnitude e incluso 
# normalizarlos con normalize:
print((r1 ^ v1).magnitude())
print((r1 ^ v1).normalize())

##_________ Exercise _________##
# Usando directamente la fórmula para la derivada en ejes móviles:
    # $$\left(\frac{\operatorname{d}\!\mathbf{a}}{\operatorname{d}\!t}\right)_1 
    # = \left(\frac{\operatorname{d}\!\mathbf{a}}{\operatorname{d}\!t}\right)_0 
    # + \mathbf{\omega}_{01}\! \times \mathbf{a}$$
# Calcula la derivada del vector de posición $R \mathbf{i}_0$, siendo $A_0$ un 
# sistema de referencia que gira respecto al inercial con velocidad angular 
# $\mathbf{\omega}_{01}=\Omega \mathbf{k}_0$. **¿Cuál es el módulo de la derivada?**
R, Omega = symbols('R, Omega', positive=True)
A0 = IJKReferenceFrame('0')
a = R * A0.i
omega01 = Omega * A0.k
da = omega01 ^ a # cross producut
print(da.magnitude())
# Si no especificaste `positive=True` vas a ver algo como sqrt(omega^2*R^2). 
# Debería haber una forma de simplificar esta expresión _a posteriori_, pero de
# momento no funciona del todo bien. 

##_________ Relative Movement _________##
# ¿A quién no le gusta multiplicar matrices de rotación? Para esa minoría que lo 
# detesta, existe SymPy. Para ello debemos especificar la orientación de nuestros 
# sistemas de referencia usando el *método orient*, y recuperaremos la matriz de 
# cosenos directores usando el *método dcm*.
A1 = IJKReferenceFrame("1")
A0 = IJKReferenceFrame("0")
phi = symbols('phi')
A0.orient(A1, 'Axis', [phi, A1.z])  # Rotación phi alrededor del eje A1.z
print(A0.dcm(A1))                          # "Direct Cosine Matrix"
# Usando el argumento `Axis` hemos especificado que rotamos el sistema un ángulo 
# especificado alrededor de un eje. Otros métodos son:
    # * `Body`: se especifican los tres ángulos de Euler.
    # * `Space`: igual que `Body`, pero las rotaciones se aplican en orden inverso.
    # * `Quaternion`: utilizando cuaternios, rotación alrededor de un vector unitario
    # $\lambda$ una cantidad $\theta$.

##_________ Different Reference System _________##
# Para expresar un vector en otro sistema de referencia, no hay más que usar los 
# métodos express o to_matrix:
print(A0.x.express(A1))
print(A0.x.to_matrix(A1))

##_________ Dynamic Symbols (time dependent) _________##
# Si queremos especificar que un símbolo puede variar con el tiempo, hay que usar 
# la función dynamicsymbols:
from sympy.physics.mechanics import dynamicsymbols

alpha = dynamicsymbols('alpha')
# Y pedir su derivada con el método diff:
print(alpha.diff())

##_________ Exercise1 _________##
print('_______________Exercise1___________________')
# from notebook completos/041-SymPy
## Obtener la matriz de rotación de la pala B respecto a los ejes A1. ##
print('______Rot Matrix_________')
A = IJKReferenceFrame("A")
A1 = IJKReferenceFrame("A1")
psi = dynamicsymbols('psi')
A1.orient(A, 'Axis', [psi, A.z])
print('A1 DCM A --> =', A1.dcm(A))  # T_{A1A}

A2 = IJKReferenceFrame("A2")
beta = dynamicsymbols('beta')
A2.orient(A1, 'Axis', [beta, -A1.y])
print('A2 DCM A1 --> =', A2.dcm(A1))  # T_{A2A1}

A3 = IJKReferenceFrame("A3")
zeta = dynamicsymbols('zeta')
A3.orient(A2, 'Axis', [zeta, A2.z])
print('A3 DCM A1 --> =',A3.dcm(A1))  # T_{A3A1}

B = IJKReferenceFrame("B")
theta = dynamicsymbols('theta')
B.orient(A3, 'Axis', [theta, A3.x])
print('B DCM A3 --> =', B.dcm(A3))  # T_{BA3}

print('B DCM A2 --> =',B.dcm(A2))

print('B DCM A1 --> =',B.dcm(A1))

## Angular Velocity ##
print('______Ang Vel______')
# También podemos hallar la velocidad angular de un sistema respecto a otro 
# usando el método ang_vel_in:
print(B.ang_vel_in(A2))
print(B.ang_vel_in(A))
print(B.ang_vel_in(A).express(A))

## Derivative in moving axis ##
print('______Derivative in moving axis______')
# Hacer una derivada con la fórmula lo hace cualquiera, pero SymPy puede 
# encargarse automáticamente.
v1 = A1.x
dv1 = v1.diff(symbols('t'), A)
print(dv1.to_matrix(A1))
print((dv1 & A1.j).simplify())
print('_______________End Exercise1___________________')

##_________ Puntos, velocidades y la rueda que no desliza _________##
# El último paso que nos queda para completar la cinemática es la posibilidad de 
# definir puntos en sólidos y aplicar su campo de velocidades. SymPy también 
# permite esto, y para ello no tenemos más que importar la clase Point.
from sympy.physics.mechanics import Point
O = Point("O")
# Para trabajar como lo haríamos en la escuela, vamos a especificar que O es el
# origen de A, y para eso vamos a imponer que su velocidad es cero con el método set_vel:
O.set_vel(A, 0)
# Para definir nuevos puntos, podemos utilizar el método locate_new:
e_b = symbols('e_b')
E_b = O.locatenew('E_b', e_b * A1.x)
# Y para obtener vectores de un punto a otro, el método pos_from:
print(E_b.pos_from(O))
# La notación de este paquete está influenciada por el libro
#  Kane, T. R. & Levinson, D. A. "Dynamics, Theory and Applications"

# Por último, el **campo de velocidades de un sólido rígido** se formula usando 
# el método `v2pt_theory`.
    # $$v^P_A = v^O_A + \omega_{A_1 A} \times \mathbf{OP}$$
# Este método pertenece *al punto del cual queremos conocer la velocidad* y 
# recibe tres parámetros:
    # * `O`, punto de velocidad conocida respecto a A
    # * `A`, sistema de referencia donde queremos calcular la velocidad
    # * `A1`, sistema de referencia donde están fijos ambos puntos (_sistema de arrastre_)
print(E_b.v2pt_theory(O, A, A1))

##_________ Exercise2 _________##
print('_______________Exercise2___________________')
# from notebook completos/041-SymPy
# ¡Halla la velocidad y la aceleración de P!

# Creamos nuestros sistemas de referencia
A1 = IJKReferenceFrame('1')
A0 = IJKReferenceFrame('0')
A2 = IJKReferenceFrame('2')

# Creamos los símbolos dinámicos necesarios
xi, theta = dynamicsymbols('xi, theta')

# Orientamos los sistemas de referencia
A0.orient(A1, 'Axis', [0, A1.k])  # A0 no gira respecto a A1
A2.orient(A0, 'Axis', [theta, A0.k])
print('A2 DCM A1 --> =', A2.dcm(A1))

# Creamos el punto C, centro del disco, y especificamos su velocidad
# respecto a A1
C = Point('C')
C.set_vel(A1, xi.diff() * A1.x)

# Localizamos el punto P, punto fijo del disco, respecto a C, en
# el sistema A2 (que gira solidariamente con el disco)
R = symbols('R')
P = C.locatenew('P', -R * A2.j)
print(P.pos_from(C))

# Hallamos la velocidad de P en A1, expresada en A0
# ¡Con esta llamada ya estamos diciendo que C y P son fijos en A2!
print(P.v2pt_theory(C, A1, A2).express(A0))

#______________________________________________________________________________
#______________________________________________________________________________
# 
# Estabilidad y control dinámicos longitudinales en cadena abierta
# Análisis de la estabilidad longitudinal de un B747-100
# https://nbviewer.jupyter.org/github/AlexS12/Mecanica_Vuelo/blob/master/MVII_MatrizSistema.ipynb