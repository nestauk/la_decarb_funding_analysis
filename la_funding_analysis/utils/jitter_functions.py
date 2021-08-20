# File: utils/jitter_functions.py
"""Functions to enable the creation of jitter plots with the jitter in a single direction.
"""

import numpy as np


def rand_jitter(list, deviation):
    """Function to add small variation to values in a list."""
    return list + np.random.randn(len(list)) * deviation


def jitter(axes, x, y, s=20, c="b", alpha=None, zorder=5, deviation=0.05, **kwargs):
    """Function to make a jitter plot, with jitter only in the x direction."""
    return axes.scatter(
        rand_jitter(x, deviation), y, s=s, c=c, alpha=alpha, zorder=zorder, **kwargs
    )
