import numpy as np

g = 9.81 # acceleration due to gravity

#_____________________________________________________________________________#
# We begin defining the main function
def main(angle=45, rel_tol=1E-3):
    # Convert the angle to radians
    angle = np.radians(45)
    
    # The method is based on knowing where we landed the previous time (v0, d0),
    # and where we did on this one (v1, d1), in order to get an estimate for the following
    # Therefore, we need some initial conditions to begin
    v0, d0, v1, d1 = init(angle) # init is another function that must be implemented
    
    # We ask the distance as an input to the user
    d = float(input('Where is the target? '))
    
    # We iterate until we get a solution
    while abs(d1 - d) / d > rel_tol:
        v0, d0, v1, d1 = bissection(v0, d0, v1, d1, angle, d) # bissection is another function to implement too
        
    # La imprimimos
    print('v = {} m/s -> d = {} m'.format(v1, d1))
#_____________________________________________________________________________#    
def init(angle):
    # El primer tiro puede ser sencillamente no ir a ninguna parte
    v0, d0 = 0.0, 0.0 # m/s, m
    # Y el segundo tiro, pues a 1 m/s, por que no?
    v1 = 1.0 # m/s
    d1 = shot(angle, v1) # We need a function shot() que haga de solver para un determinado tiro parabólico
    
    return v0, d0, v1, d1
#_____________________________________________________________________________#
def shot(angle, v):
    # First we obtain the x and y components of velocity
    vx, vy = v * np.cos(angle), v * np.sin(angle)

    # Using these components we can determine the flight time, t
    t = 2 * vy / g

    # And, therefore, the range
    return vx * t
#_____________________________________________________________________________#
def bissection(x_a, f_a, x_b, f_b, angle, f):
    # Reordenamos si es necesario
    if f_a > f_b:
        x_a, f_a, x_b, f_b = x_b, f_b, x_a, f_a
    
    # Obtenemos una nueva aproximacion para la velocidad
    if f_a < f < f_b:
        x_c = 0.5 * (x_a + x_b)
    else:
        x_c = 2.0 * x_b
    
    # Y el alcance correspodiente
    f_c = shot(angle, x_c)

    # Y comprobamos en que subintervalo esta
    if f_c > f:
        return x_a, f_a, x_c, f_c
    return x_b, f_b, x_c, f_c
#_____________________________________________________________________________#

main(15, 1E-3) # Or simply use main()
main()