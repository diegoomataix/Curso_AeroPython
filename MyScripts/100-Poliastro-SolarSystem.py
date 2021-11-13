"""
Create an animation of the movements of all the planets around the Sun for a whole year. Use the poliastro library
"""

from poliastro.plotting import StaticOrbitPlotter
from poliastro.bodies import Sun, Earth, Venus, Mars, Jupiter, Saturn, Mercury, Uranus, Neptune
from poliastro.twobody import Orbit
from poliastro.util import time_range
from astropy import time
import numpy as np
import matplotlib.pyplot as plt
# from poliastro.plotting import OrbitPlotter

# Create the orbits of the planets

# Sun
ss = Orbit.from_body_ephem(Sun)

# Earth
ee = Orbit.from_body_ephem(Earth)

# Venus
vv = Orbit.from_body_ephem(Venus)

# Mars
mm = Orbit.from_body_ephem(Mars)

# Jupiter
jj = Orbit.from_body_ephem(Jupiter)

# Saturn
sss = Orbit.from_body_ephem(Saturn)

# Mercury
me = Orbit.from_body_ephem(Mercury)

# Uranus
uu = Orbit.from_body_ephem(Uranus)

# Neptune
nn = Orbit.from_body_ephem(Neptune)

# Plot the orbits

# Sun
op = StaticOrbitPlotter()
op.plot(ss, label="Sun")

# Earth
op.plot(ee, label="Earth")

# Venus
op.plot(vv, label="Venus")

# Mars
op.plot(mm, label="Mars")

# Jupiter
op.plot(jj, label="Jupiter")

# Saturn
op.plot(sss, label="Saturn")

# Mercury
op.plot(me, label="Mercury")

# Uranus
op.plot(uu, label="Uranus")

# Neptune
op.plot(nn, label="Neptune")

# Show the plot
plt.show()


"""
Now do the same, but just for the largest Near Earth Objects (NEO).
"""

# Create the orbits of the NEOs

# Ceres
ce = Orbit.from_sbdb("Ceres")

# Pallas
pa = Orbit.from_sbdb("Pallas")

# Juno
ju = Orbit.from_sbdb("Juno")

# Vesta
ve = Orbit.from_sbdb("Vesta")

# Hygiea
hy = Orbit.from_sbdb("Hygiea")

# Eunomia
eu = Orbit.from_sbdb("Eunomia")

# Iris
ir = Orbit.from_sbdb("Iris")

# Flora
fl = Orbit.from_sbdb("Flora")

# Metis
mt = Orbit.from_sbdb("Metis")

# Plot the orbits

# Sun
opNEO = StaticOrbitPlotter()
opNEO.plot(ss, label="Sun")

# Ceres
opNEO.plot(ce, label="Ceres")

# Pallas
opNEO.plot(pa, label="Pallas")

# Juno
opNEO.plot(ju, label="Juno")

# Vesta
opNEO.plot(ve, label="Vesta")

# Hygiea
opNEO.plot(hy, label="Hygiea")

# Eunomia
opNEO.plot(eu, label="Eunomia")

# Iris
opNEO.plot(ir, label="Iris")

# Flora
opNEO.plot(fl, label="Flora")

# Metis
opNEO.plot(mt, label="Metis")

# Show the plot
plt.show()


"""
Now do the same, but for the moons of Jupiter around Jupiter
"""

# Create the orbits of the moons

# Io
io = Orbit.from_sbdb(Io, Jupiter)

# Europa
eu = Orbit.from_body_ephem(Europa, Jupiter)

# Ganymede
ga = Orbit.from_body_ephem(Ganymede, Jupiter)

# Callisto
ca = Orbit.from_body_ephem(Callisto, Jupiter)

# Plot the orbits

# Jupiter
opJup = StaticOrbitPlotter()
opJup.plot(jj, label="Jupiter")

# Io
opJup.plot(io, label="Io")

# Europa
opJup.plot(eu, label="Europa")

# Ganymede
opJup.plot(ga, label="Ganymede")

# Callisto
opJup.plot(ca, label="Callisto")

# Show the plot
plt.show()


"""
Now do the same, but for the moons of Saturn around Saturn
"""

# Create the orbits of the moons

# Mimas
mi = Orbit.from_body_ephem(Mimas, Saturn)

# Enceladus
en = Orbit.from_body_ephem(Enceladus, Saturn)

# Tethys
te = Orbit.from_body_ephem(Tethys, Saturn)

# Dione
do = Orbit.from_body_ephem(Dione, Saturn)

# Rhea
re = Orbit.from_body_ephem(Rhea, Saturn)

# Titan
ti = Orbit.from_body_ephem(Titan, Saturn)

# Iapetus
ia = Orbit.from_body_ephem(Iapetus, Saturn)

# Plot the orbits

# Saturn
opSat = StaticOrbitPlotter()
opSat.plot(sss, label="Saturn")

# Mimas
opSat.plot(mi, label="Mimas")

# Enceladus
opSat.plot(en, label="Enceladus")

# Tethys
opSat.plot(te, label="Tethys")

# Dione
opSat.plot(do, label="Dione")

# Rhea
opSat.plot(re, label="Rhea")

# Titan
opSat.plot(ti, label="Titan")

# Iapetus
opSat.plot(ia, label="Iapetus")

# Show the plot
plt.show()

