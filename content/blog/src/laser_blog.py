#!/usr/bin/env python

""" Image Analysis of a Laser Spot

Approximate a laser spot with a clamped elliptical gaussian intensity
function.
"""

""" The MIT License

Copyright (c) 2013 David Joy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard lib
import os
import shutil
import copy

# 3rd-party
import numpy as np

from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

THISDIR = os.path.dirname(os.path.realpath(__file__))
PLOTDIR = os.path.join(THISDIR, 'plots')

MIN_LEVEL = 0.5  # take 50% of the max for the clip window
CONTOUR_LEVEL = 0.85  # take the diameter at this contour level

FOCUS_FACTOR = 4.0  # Factor to focus the laser by

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------


def ellipse(xdata, phi, sigma0, sigma1, xoff=0, yoff=0, zscale=1, zoff=0, zmax=None):
    """ Elliptical gaussian

    :param xdata: a tuple (x coord, y coord) in pixels
    :param phi: angle from the x-axis (in radians)
    :param sigma0: first axis standard deviation
    :param sigma1: second axis standard deviation
    :param xoff: x-offset (in pixels)
    :param yoff: y-offset (in pixels)
    :param zoff: z-offset (in intensity)
    :param zscale: z-scale factor
    :param zmax: maximum z value

    :returns: Normalized gaussian at that point
    """
    A = (np.cos(phi) / sigma0)**2 + (np.sin(phi) / sigma1)**2
    B = (np.sin(phi) / sigma0)**2 + (np.cos(phi) / sigma1)**2
    C = 2 * np.sin(phi) * np.cos(phi) * (1 / sigma0**2 - 1 / sigma1**2)

    XX = xdata[0] - xoff
    YY = xdata[1] - yoff

    ZZ = zscale * np.exp( -0.5 * (A * XX**2 + B * YY**2 + C * (XX * YY))) + zoff

    if zmax is not None:
        ZZ[ZZ > zmax] = zmax
    return ZZ


def fake_data(XX, YY):
    """ Fake data for testing

    :param XX: X coordinates of the data as a 2D matrix
    :param YY: Y coordinates of the data as a 2D matrix

    :returns: a 2D matrix containing fake image intensity
    """

    phi = np.pi * 2 * (np.random.ranf() - 0.5)
    sigma0 = 8.0 * np.random.ranf() + 8.0
    sigma1 = 8.0 * np.random.ranf() + 8.0

    xoff = 8 * (np.random.ranf() - 0.5) + np.max(XX) / 2.0
    yoff = 8 * (np.random.ranf() - 0.5) + np.max(YY) / 2.0

    zscale = 255.0 * np.random.ranf()
    zoff = 1.0 * np.random.ranf()

    ZZ = ellipse(
        xdata=(XX, YY),
        phi=phi,
        sigma0=sigma0,
        sigma1=sigma1,
        xoff=xoff,
        yoff=yoff,
        zscale=zscale,
        zoff=zoff,
    )
    ZZ += 8.0 * np.random.ranf(ZZ.shape)

    ZZ[ZZ > 255.0] = 255.0
    ZZ[ZZ < 0.0] = 0.0

    params = {
        'phi': phi,
        'sigma0': sigma0,
        'sigma1': sigma1,
        'xoff': xoff,
        'yoff': yoff,
        'zoff': zoff,
        'zscale': zscale,
    }

    return ZZ, params


def main():

    # Unpack the global constants
    plotdir = PLOTDIR

    # Make a new directory
    if os.path.isdir(plotdir):
        shutil.rmtree(plotdir)
    os.makedirs(plotdir)

    # Fake some data
    XX, YY = np.mgrid[:64, :64]

    ZZ, params = fake_data(XX, YY)

    # Figure 1 - boring top down laser image
    fig1 = os.path.join(plotdir, 'laser_profile_boring.png')

    fig = plt.figure(figsize=(5, 4))
    plt.imshow(ZZ, cmap=plt.cm.hot)
    plt.savefig(fig1, pad_inches=0.0)

    # Figure 2 - 3D laser image
    # Zfit = ellipse((XX, YY), **params)

    fig2 = os.path.join(plotdir, 'laser_profile_simple.png')

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_wireframe(XX, YY, ZZ, colors=(1.0, 0, 0))
    ax.set_xlabel('x coord')
    ax.set_ylabel('y coord')
    ax.set_zlabel('intensity')

    fig.savefig(fig2, pad_inches=0.0)

    # Figure 3 - focusing the laser

    fig3 = os.path.join(plotdir, 'laser_profile_focus.png')

    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    ZZ_unfocused = ellipse(xdata=(XX, YY), **params)
    ax.plot_wireframe(XX, YY, ZZ_unfocused, colors=(1.0, 0, 0))

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    params2 = copy.deepcopy(params)

    # Focus the laser by a factor
    params2['sigma0'] = params['sigma0'] / np.sqrt(FOCUS_FACTOR)
    params2['sigma1'] = params['sigma1'] / np.sqrt(FOCUS_FACTOR)
    params2['zscale'] = params['zscale'] * FOCUS_FACTOR

    ZZ_focused = ellipse(xdata=(XX, YY), **params2)
    ax.plot_wireframe(XX, YY, ZZ_focused, colors=(1.0, 0, 0))

    fig.savefig(fig3, pad_inches=0.0)

if __name__ == '__main__':
    np.random.RandomState(56)
    main()