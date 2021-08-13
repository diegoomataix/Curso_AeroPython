###_______________________________ SymPy ___________________________________### 
# SymPy es una biblioteca de Python para matemática simbólica. Apunta a convertirse
# en un sistema de algebra computacional (CAS) con todas sus prestaciones manteniendo 
# el código tan simple como sea posible para manterlo comprensible y fácilmente extensible. 
# SymPy está escrito totalmente en Python y no requiere bibliotecas adicionales. 
# Este proyecto comenzó en 2005, fue lanzado al público en 2007 y a él han contribuido 
# durante estos años cientos de personas.

##_________________________ Creating Symbols ___________________________##
from sympy import init_session, Symbol, symbols, pi, I, E, cos, sin, exp, tan, simplify, expand, factor, collect, apart, cancel, expand_trig, diff, Derivative, Function, integrate, limit, series, Eq, solve, dsolve, Matrix, N
init_session(use_latex='matplotlib')

# Creamos el símbolo a
a = Symbol('a')
print((a + pi) ** 2)
print(type(a))
b = 2 * a
print(type(b))
print(b)
# Como Python permite que el tipo de una variable cambie, si ahora le asigno a 
# a un valor float deja de ser un símbolo
a = 2.26492
print(type(a))

# __Las conclusiones son:_
    # * __Si quiero usar una variable como símbolo debo crearla previamente.__
    # * Las operaciones con símbolos devuelven símbolos.
    # * Si una varibale que almacenaba un símbolo recibe otra asignación, cambia de tipo.
# Las variables de tipo Symbol actúan como contenedores en los que no sabemos qué 
# hay (un real, un complejo, una lista...). Hay que tener en cuenta que: una cosa es 
# el nombre de la variable y otra el símbolo con el que se representa
#creación de símbolos
coef_traccion = Symbol('c_T')
# Diferencia entre variable y símbolo
a = symbols('b')
x, y, z, t = symbols('x y z t')
#  símbolos griegos:
w = symbols('omega')
W = symbols('Omega')

# Por defecto, SymPy entiende que los símbolos son números complejos. Esto puede 
# producir resultados inesperados ante determinadas operaciones como, por ejemplo,
# lo logaritmos. Podemos indicar que la variable es real, entera... en el momento 
# de la creación

# Creamos símbolos reales
x, y, z, t = symbols('x y z t', real=True)
# Podemos ver las asunciones de un símbolo
print(x.assumptions0)

##_________________________ Expressions ___________________________##
expr = cos(x)**2 + sin(x)**2
print(expr)

# Podemos pedirle que simplifique la expresión anterior
print(simplify(expr))

# En algunas ocasiones necesitaremos sustituir una variable por otra, por otra
# expresión o por un valor, using 'subs'
# Sustituimos x por y ** 2
print(expr.subs(x, y**2))
# ¡Pero la expresión no cambia!
# Para que cambie
expr = expr.subs(sin(x), exp(x))
print(expr)
# Particulariza la expresión sin(x)+3x en x=pi
print((sin(x) + 3 * x).subs(x, pi))

# Aunque si lo que queremos es obtener el valor numérico lo mejor es .evalf()
print((sin(x) + 3 * x).subs(x, pi).evalf(25)) # Nº of decimal places is the n isnide ()

# el mismo resultado se obtiene ocn la función N()
print(N(pi,25))

##_________________________ Simplification ___________________________##
# SymPy ofrece numerosas funciones para __simplificar y manipular expresiones__.
 # Entre otras, destacan:
    # * `expand()`
    # * `factor()`
    # * `collect()`
    # * `apart()`
    # * `cancel()`
# Puedes consultar en la documentación de SymPy lo que hace cada una y algunos ejemplos.
# Existen también funciones específicas de simplificación para funciones trigonométricas,
# potencias y logaritmos. Abre [esta documentación](http://docs.sympy.org/latest/tutorial/simplification.html) si lo necesitas.

#_____________ Examples _____________##
expr1 = (x**3 + 3*y +2)**2
print(expand(expr1))

expr2 = (3*x**2 - 2*x +1) / ((x-1)**2)
print(apart(expr2))

expr3 = (x**3 + 9*x**2 +27*x + 27)
print(factor(expr3))

expr4 = sin(x + 2 * y)
print(expand_trig(expr4))
print(expand(expr4, trig=True))

##_____________ Derivatives _____________##
# Puedes derivar una expresion usando el método .diff() y la función dif()
#creamos una expresión
expr = cos(x)
#obtenemos la derivada primera con funcion
print(diff(expr, x)) #or:
print(expr.diff(x))

# Third derivative?
print(expr.diff(x,x,x))
print(expr.diff(x,3))

# Many derivatives?
expr_xy = y ** 3 * sin(x) ** 2 + x ** 2 * cos(y)
print(diff(expr_xy, x, 2, y, 2))

# Si queremos que la deje indicada, usamos Derivative()
print(Derivative(expr_xy, x, 2, y))

# Can SymPy apply the chain rule?
# Creamos una función F #
F = Function('F')
print(F(x))
# Creamos una función G
G = Function('G')
print(G(x))
# Derivamos la función compuesta F(G(x))
print(F(G(x)).diff(x))

# If we know the functions: #
# definimos una f
f = 2 * y * exp(x)
# definimos una g(f)
g = f **2 * cos(x) + f
#la derivamos
print(diff(g,x))

##_____________ Integrals _____________##
int1 = cos(x)**2
print(int1.integrate(x))

int2 = 1 / sin(x)
print(int2.integrate(x))

x, a = symbols('x a', real=True)

int3 = 1 / (x**2 + a**2)**2
print(int3.integrate(x))

##_________________________ Limits ___________________________##
# Calculemos este límite sacado del libro _Cálculo: definiciones, teoremas y 
# resultados_, de Juan de Burgos:
    # $$\lim_{x \to 0} \left(\frac{x}{\tan{\left (x \right )}}\right)^{\frac{1}{x^{2}}}$$
# Primero creamos la expresión:
x = symbols('x', real=True)
expr = (x / tan(x)) ** (1 / x**2)
#Obtenemos el límite con la función limit() y si queremos dejarlo indicado, 
# podemos usar Limit():
print(limit(expr, x, 0))
    
##_________________________ Series ___________________________##
#creamos la expresión
expr = exp(x)
print(series(expr))
# Se puede especificar el número de términos pasándole un argumento n=.... 
# El número que le pasemos será el primer término que desprecie.
# Indicando el número de términos
print(series(expr, n=10))

# Si nos molesta el O(x**10) lo podemos quitar con removeO():
print(series(expr, n=10).removeO())
print(series(sin(x), n=8, x0=pi/3).removeO().subs(x, x-pi/3))

##_________________________ Eq resolution ___________________________##
# Como se ha mencionado anteriormente las ecuaciones no se pueden crear con el =
#creamos la ecuación
equation = Eq(x ** 2 - x, 3)
# También la podemos crear como
print(Eq(x ** 2 - x -3))
# Solve it:
print(solve(equation))

# To solve using symbols: #
# Creamos los símbolos y la ecuación
a, x, t, C = symbols('a, x, t, C', real=True)
equation2 = Eq(a * exp(x/t), C)
print(solve(equation2 ,x))

##_________________________ Diff equations ___________________________##
# dsolve is the solver for differential equations
x = symbols('x')
y = Function('y')
ecuacion_dif = Eq(y(x).diff(x,2) + y(x).diff(x) + y(x), cos(x))
#resolvemos
# print(dsolve(ecuacion_dif, f(x)))

##_________________________ Matrices ___________________________##
#creamos una matriz llena de símbolos
a, b, c, d = symbols('a b c d')
A = Matrix([
            [a, b],
            [c, d]
    ])
#sacamos autovalores
print(A.eigenvals())
#inversa
print(A.inv())
#elevamos al cuadrado la matriz
print(A ** 2)
