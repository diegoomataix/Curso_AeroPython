###________________ Analyzing the Parker Solar Probe flybys ________________###
import numpy as np

from matplotlib import pyplot as plt

from astropy import units as u
from astropy.time import Time

from poliastro.ephem import Ephem
from poliastro.util import norm
from poliastro.bodies import Earth, Sun, Venus
from poliastro import iod
from poliastro.threebody.flybys import compute_flyby
from poliastro.twobody import Orbit
from poliastro.frames import Planes
from poliastro.plotting import StaticOrbitPlotter

from scipy.optimize import brentq

#__________ Modulus of the exit velocity, some features of Orbit #2 __________#

# First, using the data available in the reports, we try to compute some of the 
# properties of orbit #2. This is not enough to completely define the trajectory, 
# but will give us information later on in the process:

T_ref = 150 * u.day
k = Sun.k

# T=2*pi*sqrt(a^3/mu)−−> a=...
a_ref = np.cbrt(k * T_ref ** 2 / (4 * np.pi ** 2)).to(u.km)
a_ref.to(u.au)

# epsilon = −mu/r+v^2/2=−mu/2a −−> v=...
energy_ref = (-k / (2 * a_ref)).to(u.J / u.kg)

flyby_1_time = Time("2018-09-28", scale="tdb")

r_mag_ref = norm(Ephem.from_body(Venus, flyby_1_time).rv()[0])
v_mag_ref = np.sqrt(2 * k / r_mag_ref - k / a_ref).to(u.km / u.s)

#______________________ Lambert arc between #0 and #1 ________________________#
# To compute the arrival velocity to Venus at flyby #1, we have the necessary 
# data to solve the boundary value problem:

d_launch = Time("2018-08-11", scale="tdb")

r0, _ = Ephem.from_body(Earth, d_launch).rv()
r1, V = Ephem.from_body(Venus, flyby_1_time).rv()

r0 = r0[0]
r1 = r1[0]
V = V[0]

tof = flyby_1_time - d_launch

((v0, v1_pre),) = iod.lambert(Sun.k, r0, r1, tof.to(u.s))
print(norm(v1_pre))

#___________________________ Flyby #1 around Venus ___________________________#
# We compute a flyby using poliastro with the default value of the entry angle, 
# just to discover that the results do not match what we expected:
    
V.to(u.km / u.day)
h = 2548 * u.km
d_flyby_1 = (Venus.R + h).to(u.km)

V_2_v_, delta_ = compute_flyby(v1_pre, V, Venus.k, d_flyby_1)
print(norm(V_2_v_))

#_______________________________ Optimization ________________________________#
# Now we will try to find the value of theta that satisfies our requirements:

def func(theta):
    V_2_v, _ = compute_flyby(v1_pre, V, Venus.k, d_flyby_1, theta * u.rad)
    ss_1 = Orbit.from_vectors(Sun, r1, V_2_v, epoch=flyby_1_time)
    
    return (ss_1.period - T_ref).to(u.day).value

# There are two solutions:
theta_range = np.linspace(0, 2 * np.pi)
plt.plot(theta_range, [func(theta) for theta in theta_range])
plt.axhline(0, color="k", linestyle="dashed");
plt.show()

print(func(0))
print(func(1))

theta_opt_a = (brentq(func, 0, 1) * u.rad).to(u.deg)
theta_opt_b = (brentq(func, 4, 5) * u.rad).to(u.deg)

V_2_v_a, delta_a = compute_flyby(v1_pre, V[0], Venus.k, d_flyby_1, theta_opt_a)
V_2_v_b, delta_b = compute_flyby(v1_pre, V[0], Venus.k, d_flyby_1, theta_opt_b)

print(norm(V_2_v_a))
print(norm(V_2_v_b))

#________________________________ Exit Orbit _________________________________#
# And finally, we compute orbit #2 and check that the period is the expected one:
    
ss01 = Orbit.from_vectors(Sun, r1, v1_pre, epoch=flyby_1_time)

# The two solutions have different inclinations, so we still have to find out 
# which is the good one. We can do this by computing the inclination over the 
# ecliptic - however, as the original data was in the International Celestial 
# Reference Frame (ICRF), whose fundamental plane is parallel to the Earth 
# equator of a reference epoch, we have to change the plane to the Earth ecliptic, 
# which is what the original reports use:
    
ss_1_a = Orbit.from_vectors(Sun, r1, V_2_v_a, epoch=flyby_1_time)

ss_1_b = Orbit.from_vectors(Sun, r1, V_2_v_b, epoch=flyby_1_time)

print(ss_1_a.change_plane(Planes.EARTH_ECLIPTIC))
print(ss_1_b.change_plane(Planes.EARTH_ECLIPTIC))

# Therefore, the correct option is the first one:
print(ss_1_a.period.to(u.day))
print(ss_1_a.a)

# And, finally, we plot the solution:
frame = StaticOrbitPlotter(plane=Planes.EARTH_ECLIPTIC)

frame.plot_body_orbit(Earth, d_launch)
frame.plot_body_orbit(Venus, flyby_1_time)
frame.plot(ss01, label="#0 to #1", color="C2")
frame.plot(ss_1_a, label="#1 to #2", color="C3");