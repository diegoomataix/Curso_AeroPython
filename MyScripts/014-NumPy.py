### LINEAR ALGEBRA ###
import numpy as np
# from numpy.linalg import norm, det
# help(np.linalg)

# M = np.array([
#     [1, 2],
#     [3, 4]
# ])
# v = np.array([1, -1])

# # print(v.T) # Calcular transpuesta no funciona al ser vector (matriz 1D)

# u = np.dot(M, v)

# # Para hacer comparaciones entre arrays de punto flotante se puede usar:
# # np.allclose: comprueba si todos los elementos de los arrays son iguales dentro de una tolerancia, 
# # np.isclose: compara elemento a elemento y devuelve un array de valores True y False
# # np.allclose(u, v)
# # np.isclose(0.0, 1e-8, atol=1e-10)

# # u = M @ v # Hace operaciones entre matrices
# # print(u)

# mat = np.array([[1, 5, 8, 5],
#                 [0, 6, 4, 2],
#                 [9, 3, 1, 6]])

# vec1 = np.array([5, 6, 2])

# print(vec1 @ mat)

## Exercise 1 ##
# Hallar el producto de estas dos matrices y su determinante:

# A = np.array([
#     [1, 0, 0],
#     [2, 1, 1],
#     [-1, 0, 1]
# ])
# B = np.array([
#     [2, 3, -1],
#     [0, -2, 1],
#     [0, 0, 3]
# ])

# C = A @ B
# determ = det(C)

## Exercise 2 ##
# 2- Resolver el siguiente sistema:

# $$ \begin{pmatrix} 2 & 0 & 0 \\ -1 & 1 & 0 \\ 3 & 2 & -1 \end{pmatrix} \begin{pmatrix} 1 & 1 & 1 \\ 0 & 1 & 2 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -1 \\ 3 \\ 0 \end{pmatrix} $$
# M = (np.array([[2, 0, 0],
#                         [-1, 1, 0],
#                         [3, 2, -1]])
#      @
#         np.array([[1, 1, 1],
#                         [0, 1, 2],
#                         [0, 0, 1]]))
# res = np.array([-1, 3, 0])

# x = np.linalg.solve(M,res)

# print(np.allclose(M @ x, res))

## Exercise 3 ##
# 3- Hallar la inversa de la matriz 𝐻 y comprobar que 𝐻𝐻−1=𝐼 (recuerda la función np.eye)
# A = np.arange(1, 37).reshape(6,6)
# A[1, 1::2] = 0
# A[3, ::2] = 1
# A[4, :] += 30
# B = (2 ** np.arange(36)).reshape((6,6))
# H = A + B
# print(H)

# print(np.linalg.det(H))

# Hinv = np.linalg.inv(H)

# np.isclose(np.dot(Hinv, H), np.eye(6))

# np.set_printoptions(precision=3)
# print(np.dot(Hinv, H))

#¡No funciona! Y no solo eso sino que los resultados varían de un ordenador a otro.

## Exercise 4 ##
# print(np.linalg.cond(H))
# La matriz está mal condicionada

## Exercise 5 ## # Autovalores y autovectores #
A = np.array([
    [1, 0, 0],
    [2, 1, 1],
    [-1, 0, 1]
])

eigen = np.linalg.eig(A)
