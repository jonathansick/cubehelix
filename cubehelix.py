# -*- coding: utf-8 -*-
from matplotlib.colors import LinearSegmentedColormap as LSC
from math import pi
import numpy as np

def cmap(start=0.5, rot=-1.5, gamma=1.0, hue=1.2, reverse=False):
    """
    A full implementation of Dave Green's "cubehelix" for Matplotlib.
    Based on the FORTRAN 77 code provided in 
    D.A. Green, 2011, BASI, 39, 289. 
    
    http://adsabs.harvard.edu/abs/2011arXiv1108.5083G

    User can adjust all parameters of the cubehelix algorithm. 
    This enables much greater flexibility in choosing color maps, while 
    always ensuring the color map scales in intensity from black 
    to white. A few simple examples:
    
    Default color map settings produce the standard "cubehelix".

    Create color map in only blues by setting rot=0 and start=0.

    Create reverse (white to black) backwards through the rainbow once
    by setting rot=1 and reverse=True.
    

    Parameters
    ----------
    start : scalar, optional
        Sets the starting position in the color space. 0=blue, 1=red, 
        2=green. Defaults to 0.5.
    rot : scalar, optional
        The number of rotations through the rainbow. Can be positive 
        or negative, indicating direction of rainbow. Negative values
        correspond to Blue->Red direction. Defaults to -1.5
    gamma : scalar, optional
        The gamma correction for intensity. Defaults to 1.0        
    hue : scalar, optional
        The hue intensity factor. Defaults to 1.2
    reverse : boolean, optional
        Set to True to reverse the color map. Will go from black to
        white. Good for density plots where shade~density. Defaults to False

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap object

    Example
    -------
    >>> import cubehelix
    >>> cx = cubehelix.cmap(start=0., rot=-0.5)
    >>> plot(x,cmap=cx)

    Revisions
    ---------
    2014-04-16 (jradavenport) Ported from IDL version
    """

    nlev = 256.

#-- set up the parameters
    fract = np.arange(nlev)/(nlev-1.)
    angle = 2.0*pi * (start/3.0 + 1.0 + rot*fract)
    fract = fract**gamma
    amp   = hue*fract*(1.-fract)/2.

#-- compute the RGB vectors according to main equations
    red   = fract+amp*(-0.14861*np.cos(angle)+1.78277*np.sin(angle))
    grn   = fract+amp*(-0.29227*np.cos(angle)-0.90649*np.sin(angle))
    blu   = fract+amp*(1.97294*np.cos(angle))

#-- find where RBB are outside the range [0,1], clip
    red[np.where((red > 1.))] = 1.   
    grn[np.where((grn > 1.))] = 1.   
    blu[np.where((blu > 1.))] = 1.

    red[np.where((red < 0.))] = 0.   
    grn[np.where((grn < 0.))] = 0.   
    blu[np.where((blu < 0.))] = 0.

#-- optional color reverse
    if reverse==True:
        red = red[::-1]
        blu = blu[::-1]
        grn = grn[::-1]

#-- put in to tuple & dictionary structures needed
    rr = []
    bb = []
    gg = []
    for k in range(0,int(nlev)):
        rr.append((float(k)/(nlev-1.), red[k], red[k]))
        bb.append((float(k)/(nlev-1.), blu[k], blu[k]))
        gg.append((float(k)/(nlev-1.), grn[k], grn[k]))
    
    cdict = {'red':rr, 'blue':bb, 'green':gg}
    return LSC('cubehelix_map',cdict)