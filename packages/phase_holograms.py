"""Module containing the functions for generating holograms"""
import numpy as np 
from scipy.special import jv
from scipy.optimize import root_scalar


def _holo_preamble(field, nuvec, renorm=True):
    
    sh = field.shape
    x,y = np.meshgrid(np.arange(sh[1]),np.arange(sh[0]))
    phase_s = np.exp(1j * 2 * np.pi * (nuvec[0]*x + nuvec[1]*y))
    a = np.abs(field)
    phi = np.angle(field * phase_s)
    # nunorm = 2*np.linalg.norm(nuvec)
    if renorm:
        a /=np.max(a)
    return a, phi#, x-nuvec[1]/nunorm, y+nuvec[0]/nunorm

# Holograms presented in JOSA A 24 3500, 2007

def find_fa(holo_type='one'):
    y_samp = np.linspace(0,1,50)
    if holo_type == 'one':
        fa = np.array([root_scalar(lambda x: np.sinc(1-x) - 1 * y_samp[ii],
                                      bracket=[-1, 1], method='brentq').root
                            for ii in range(len(y_samp))])
    elif holo_type == 'two':
        # func = lambda x, y: jv(0, x) - 0.99 * y
        fa = np.array([root_scalar(lambda x: jv(0, x) - 1 * y_samp[ii],
                                      bracket=[0, 4], method='brentq').root
                            for ii in range(len(y_samp))])
    elif holo_type == 'three':
        fa = np.array([root_scalar(lambda x: jv(1, x) - 0.581 * y_samp[ii],
                                      bracket=[0, 1.85], method='brentq').root
                            for ii in range(len(y_samp))])
    else:
        raise ValueError('Invalid option for holo_type.')
    
    return np.poly1d(np.polyfit(y_samp, fa, 10))





def hologram_type1(field, nuvec, fa=None):
    if fa is None:
        fa = find_fa(holo_type='one')
    a, phi = _holo_preamble(field, nuvec)
    return np.mod(fa(a)* phi, 2*np.pi)

def hologram_type2(field, nuvec, fa=None):
    if fa is None:
        fa = find_fa(holo_type='two')
    a, phi = _holo_preamble(field, nuvec)
    return np.mod(phi + fa(a)* np.sin(phi)+np.pi, 2*np.pi)

def hologram_type3(field, nuvec, fa=None):
    if fa is None:
        fa = find_fa(holo_type='three')
    a, phi = _holo_preamble(field, nuvec)
    return np.mod(fa(a)* np.sin(phi)+1*np.pi, 2*np.pi)-0*np.pi