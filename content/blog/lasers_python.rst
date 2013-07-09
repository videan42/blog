Python and Lasers
#################

:date: 2013-07-03
:tags: python, images, lasers
:author: David Joy
:lang: en
:summary: Analyse a Laser Image in Python
:latex:

I never know what to talk about in the first blog post, so I figured today I would talk about lasers.

Image Analysis of a Laser Spot
==============================

A friend of mine was trying to calibrate her laser system, so I offered to help out with the data analysis. For reference, here's what a laser looks like.

.. image:: /static/blog/images/laser_profile_boring.png
    :alt: Booooooooring...

Yeah, it's a dot on a wall. Not super interesting. Let's look at a better view.

.. image:: /static/blog/images/laser_profile_simple.png
    :alt: Maybe less boring?

Okay, that's better. A quick trip to `Wikipedia <http://en.wikipedia.org/wiki/Beam_diameter>`_ suggests that we can measure a laser with a normally distributed beam with an elliptical cross section. After eyeballing the data... that seems like a decent model to me.

((Full disclosure: I faked the above data with numpy. I promise that it looks like the real images, but you'll have to take my word))

.. code-block:: python

    XX, YY = np.mgrid[:64, :64]

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

Okay, let's walk through what's happening. `numpy.random.ranf <http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.ranf.html>`_ generates a random float between 0 and 1. We use that to spit out the parameters for an Elliptical Gaussian function, in particular, one centered on ``xoff``, ``yoff`` with magnitude ``zscale`` and axes ``sigma0``, ``sigma1``.  Then we corrupt it with a small amount of random noise. Okay, so what's happening in ``ellipse``?

.. code-block:: python

    def ellipse(xdata, phi, sigma0, sigma1, xoff=0, yoff=0, zscale=1, zoff=0):
        """ Elliptical gaussian """

        A = (np.cos(phi) / sigma0)**2 + (np.sin(phi) / sigma1)**2
        B = (np.sin(phi) / sigma0)**2 + (np.cos(phi) / sigma1)**2
        C = 2 * np.sin(phi) * np.cos(phi) * (1 / sigma0**2 - 1 / sigma1**2)

        XX = xdata[0] - xoff
        YY = xdata[1] - yoff

        ZZ = zscale * np.exp( -0.5 * (A * XX**2 + B * YY**2 + C * (XX * YY))) + zoff

        return ZZ

Elliptical gaussian in 6-lines of python. Sweet.

Anyway, my friend wanted to know whether her lens was working. In particular, the lens should take the laser beam and focus it like this.

.. image:: /static/blog/images/laser_profile_focus.png
    :alt: focus!

Note how much narrower the beam is, and also how the peak has increased. In particular, focusing should conserve energy, aka that area under the curve thing

$$x^2$$