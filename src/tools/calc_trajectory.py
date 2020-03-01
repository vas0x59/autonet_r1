import numpy as np
import scipy
from  matplotlib  import pyplot as plt
from scipy.special import comb
from autonet_r1.src.tools.tf_tools import *
def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals

def duga_calc(p1, p2, v=0):
    if v == 0:
        coords = np.array([p1, [max(p1[0], p2[0]), min(p1[1], p2[1])], p2])
    else:
        coords = np.array([p1, [min(p1[0], p2[0]), max(p1[1], p2[1])], p2])
    new_x, new_y = bezier_curve(coords, nTimes=10)
    new_coords = np.vstack([new_x, new_y]).T
    return new_coords

def find_trajectory(p1, p2, yaw):
    c1 = np.flip(duga_calc(p1, p2, v=0), 0)
    c2 = np.flip(duga_calc(p1, p2, v=1), 0)
    a1 = math.atan2(c1[1][1] - p1[1], c1[1][0] - p1[0])
    a2 = math.atan2(c2[1][1] - p1[1], c2[1][0] - p1[0])
    if abs(offset_yaw(a1, yaw)) < abs(offset_yaw(a2, yaw)):
        return c1
    else:
        return c2
    # p1