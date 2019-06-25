"""Test parameters description file"""

import pytest
import numpy as np

from ocelot import *
from ocelot.cpbd.beam import generate_parray
from ocelot.utils.acc_utils import chicane_RTU

"""Lattice elements definition"""

D0 = Drift(l=0.1, eid = 'D0')
D1 = Drift(l=0.1, eid = 'D1')
D2 = Drift(l=0.5)
D3 = Drift(l=1.)

BL_48I_I1 = SBend(l=0.200330283531, angle=-0.099484, e1=0.0, e2 = -0.099484, tilt=0.0, fint=0.0, eid='BL.48I.I1')
BL_48II_I1 = SBend(l=0.200330283531, angle=0.099484, e1=0.099484, e2 = 0.0, tilt=0.0, fint=0.0, eid='BL.48II.I1')
BL_50I_I1 = SBend(l=0.200330283531, angle=0.099484, e1=0.0, e2 = 0.099484, tilt=0.0, fint=0.0, eid='BL.50I.I1')
BL_50II_I1 = SBend(l=0.200330283531, angle=-0.099484, e1=-0.099484, e2 = 0.0, tilt=0.0, fint=0.0, eid='BL.50II.I1')

UNDU = Undulator(lperiod=0.074, nperiods=10, Kx=1.36*1.414213, Ky=0.0, eid='UNDU')

und_start = Marker()
und_stop = Marker()

"""pytest fixtures definition"""

@pytest.fixture(scope='module')
def cell():
    return (D0, BL_48I_I1, D1, BL_48II_I1, D2, und_start, UNDU, und_stop, D2, BL_50I_I1, D1, BL_50II_I1, D3)


@pytest.fixture(scope='module')
def method():
    
    m = MethodTM()
    m.global_method = SecondTM
    
    return m
    
    
@pytest.fixture(scope='module')
def lattice(cell, method):
    return MagneticLattice(cell, method=method)


@pytest.fixture(scope='function')
def p_array():

    np.random.seed(11)

    # generate beam file
    sigma_x = 0.000121407185261
    sigma_px = 1.80989470506e-05
    sigma_y = 0.000165584800564
    sigma_py = 4.00994225888e-05

    p_array = generate_parray(sigma_x=sigma_x, sigma_px=sigma_px, sigma_y=None, sigma_py=None,
                              sigma_tau=1.30190131e-04, sigma_p=3.09815718e-04, chirp=0.002, charge=0.5e-9,
                              nparticles=20000, energy=0.13)

    return p_array