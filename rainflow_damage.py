import math
import operator
import numpy as NP
import scipy.integrate
import scipy.special
import csv
import simpson
import logging

def read_element_stress_PSD(fname):
    stress_PSD = []
    f = open(fname,'r')
    rdr = csv.reader(f)
    for freq, s_PSD in rdr:
        stress_PSD.append((float(freq), float(s_PSD)))
    f.close()
    return stress_PSD

class StressPSD(object):
    def __init__(self, stress_PSD):
        self.stress_PSD = dict(stress_PSD)
        sorted_lst = sorted(self.stress_PSD.iteritems())
        f = NP.array(map(operator.itemgetter(0), sorted_lst))
        vals = NP.array(map(operator.itemgetter(1), sorted_lst))
        self.M0 = scipy.integrate.trapz(vals, x = f) 
        self.M2 = scipy.integrate.trapz(f*f*vals, x = f)
        self.M4 = scipy.integrate.trapz(f*f*f*f*vals, x = f)
        self.nu_0_plus = math.sqrt(self.M2/self.M0) # rate of zero crossings
        self.nu_p = math.sqrt(self.M4/self.M2) # rate of peaks
        self.alpha = self.nu_0_plus/self.nu_p # irregularity factor
        self.epsilon = math.sqrt(1.0-self.alpha*self.alpha) # spectral width parameter
        
class Material(object):
    def __init__(self, A, m):
        self.A = A
        self.m = m
        
SQRT2 = math.sqrt(2.0)

def damage(s_psd, T, material):
    '''
    Wirshing and Light empirical equivalent narrow band model
    Note that the RMS Stress is converted to ksi since the material data is in ksi
    Note also that A is based on amplitude, not range
    '''
    d_nb = (s_psd.nu_0_plus*T/material.A)*pow((SQRT2*math.sqrt(s_psd.M0)/1000.0),material.m)*scipy.special.gamma(material.m/2.0+1.0)
    a_m = 0.926 - 0.033*material.m
    b_m = 1.587*material.m - 2.323
    _lambda = a_m + (1 - a_m)*pow(1 - s_psd.epsilon, b_m)
    return _lambda*d_nb

if __name__ == '__main__':
    stress_PSD = read_element_stress_PSD('element.csv')
    mtrl = Material(A=pow(10.0,24.49), m = 9.62)
    s_PSD = StressPSD(stress_PSD)
    print 'damage: %s' % (damage(s_PSD, 3600.0, mtrl))
    pass
