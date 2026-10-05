"""
To use this file, make sure that SnapPy is installed,
and the latest Spherogram is installed from GitHub using:
$ pip install --upgrade git+https://github.com/3-manifolds/Spherogram

Decompress the file sln1_matrices.tar.bz2 and change the variable
dir_R_matrices to the direcotry containing the folder sln1.

Either execute this file in Sage or Python (wherever SnapPy and Spherogram is installed),
or launch their kernels in the same directory of this file and do::

    >>> from sln1 import *

After importing, the following method computes the sln1  polynomial::

    >>> sln1(2, '3_1') # The sl21 polynomial of the trefoil
    t^2 - t - t*q^-1 + 1 + 2*q^-1 - t^-1*q^-1 - t^-1*q^-2 + t^-2*q^-2

The input can either be the name of a knot in SnapPy's database, or a snappy.Link instance::

    >>> K = snappy.Link([(5, 2, 0, 3), (3, 0, 4, 1), (1, 4, 2, 5)])
    >>> sln1(2, K)
    t^2 - t - t*q^-1 + 1 + 2*q^-1 - t^-1*q^-1 - t^-1*q^-2 + t^-2*q^-2
"""

from spherogram import RMatrix
import snappy, os

dir_R_matrices = "/Users/data/R_matrices"

_cache = dict()

def sln1_R_matrices(n, sage_polynomials=False):
    if 1 < n <= 5:
        key = (f"sl{n}1", sage_polynomials)
        if key in _cache.keys():
            return _cache[key]
        else:
            _cache[key] = RMatrix.from_directory(
                dir_path=os.path.join(dir_R_matrices, f"sl{n}1/"),
                vars=["t", "q"],
                compressed=False,
                sage_polynomials=sage_polynomials,
            )
            return _cache[key]
    else:
        raise NotImplementedError

def sln1(n, K, sage_polynomials=False):
    if isinstance(K, str):
        K = snappy.Link(K)
    elif not isinstance(K, snappy.Link):
        raise NotImplementedError

    T = K.min_long_diagram()

    return T.reshetikhin_turaev_network(
        sln1_R_matrices(n, sage_polynomials=sage_polynomials)
    ).evaluate()[0]
