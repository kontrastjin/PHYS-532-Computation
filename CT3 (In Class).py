# -*- coding: utf-8 -*-
"""
/////////////////////////////////////////////////////////////////
Matthew R. Myers             PHYS 532       CT2        (9.2.2016)
/////////////////////////////////////////////////////////////////

OBJ: Plot the electric field of a distribution of charge
"""

#Import library numpy
import numpy
#Import library matplotlib's method pyplot, but renamed as plt
import matplotlib.pyplot as plt
#Import library matplot's method patches
from matplotlib.patches import Circle
import random

# Electric Field is a measure of the physical realm of the affective strength of the (attractive/repulsive) force impartable to a charged particle by another system of charge, it is essentially a linear combination of charge and vector displacement to and from. 
# E(r) =(1/4*pi*ep_0)*SUM{i=1->n}(q_i*(r^_i)/(r_i**2))


# Define method "Efield" to return the values of the electric field along what would be field lines
def Efield(q, r0, x, y):
    # Efield is function of charge at r0 = (x0,y0) to field affect at r = (x,y)
    # Displacement magnitude from r0 -> r "disp" = ((x - x0)**2 + (y - y0)**2)
    # Displacement vector uses trig components where r_x = (x-x0)/disp & r_y = (y-y0)/disp
    # E(x) = q*(1/(disp**2))*r_x => q*(x-x0)/(disp**1.5)
    # E(y) = q*(1/(disp**2))*r_y => q*(y-y0)/(disp**1.5)
    
    disp = ((x - r0[0])**2 + (y - r0[1])**2) # where r0[0] = x0 & r0[1] = y0
    # Efield ends with returning output to python the field line values for all given x,y
    return q * (abs(x - r0[0])) / disp**1.5, q * (y - r0[1]) / disp**1.5

# To create distribution of a line of given length "L" of charge with linear charge density lambda (which is either given as lambda(r) or uniform lambda = Q/L) use numpy's linspace which generates a given number of points "steps" as a sequence of values in between a given a to b where "a" = -L/2 & "b"= L/2 (as to have line equidistantly split by origin along x with y = 0).
# Define method "qDistribution" to create list of charge values at locations x,y
def qDistribution():
    dim = 2    
    L = 8*dim
    steps = 512         
    nx, ny = steps, steps  #Setup number of samples to generate
    x = numpy.linspace(-dim, dim, nx)
    y = numpy.linspace(-dim, dim, ny)
    X, Y = numpy.meshgrid(x, y) # 2D plot space for E generated

    charges = list()
    for i in range(0,steps):
        q = (1/steps)*numpy.linspace((-L/2),(L/2),steps)
        x0 = random.uniform((-L/2), (L/2)) # generates floating number between range stated in parentheses
        y0 = 0
        charges.append((q, (x0, y0)))

#Plotting (x,y) coordinates of defined field one by one, starting with E-Field array filled with zeroes for variable q at all (x,y)
    Ex, Ey = numpy.zeros((ny, nx)), numpy.zeros((ny, nx))
    for q, pos in charges:
        ex, ey = Efield(q, pos, X, Y) #
        Ex += ex
        Ey += ey

    return charges, x, y, Ex, Ey

### Plotting
def plot_charges(charges, x, y, Ex, Ey, d):
    """
    Create plot from:
        charges = [(charge_dq, (x_pos, y_pos)), ...]
        x, y, setup base plot
        Ex, Ey, setup electric field plot
        Densiy of electric field lines decided by d=#, d=2 default, d=4 "double"
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    color = numpy.log(numpy.sqrt(Ex ** 2 + Ey ** 2))
    ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.hot, density=d, arrowstyle='->', arrowsize=1.5)

    charge_colors = {True: '#aa0000', False: '#0000aa'}
    for q, pos in charges:
        ax.add_artist(Circle(pos, 0.05, color=charge_colors[q > 0]))

    lim = 2
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    plt.show()


plot_charges(*qDistribution(), d=2)

#References:
# [1] Matthew Rothfuss, mrengr@ksu.edu
# [2] David J. Griffiths - Introducation to Electrodynamics 4th Ed. (2014)
# [3] http://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html
# [4] http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.linspace.html
# [5] https://docs.python.org/2/library/random.html#random.uniform
# [6] Filip Garner