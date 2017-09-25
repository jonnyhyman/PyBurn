import numpy as np
import Properties as chem
"""
    Ref 0 http://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1079&context=mae_facpub
    Ref 1 http://www.d.umn.edu/~rrosandi/Hybrids/Reports/Numerical_Model.pdf
    Ref 2 http://www.enu.kz/repository/2011/AIAA-2011-5909.pdf
    Ref 3 https://www.fire.tc.faa.gov/pdf/05-14.pdf
    Ref 4 https://goo.gl/1Eh1Gf

    Rocket Propulsion Elements, https://goo.gl/kCFbHc
"""
# ----------------------------------------------------- Nozzle Design Analysis
class Nozzle(object):

    g0 = 9.80665

    def evaluate(n,input):
        """ Optimal nozzle design analysis """

        mdot = input['mdot']
        OF   = input['OF']
        p1   = input['p1']
        p2   = input['p3']       # assume p2 == p3
        At   = input['At']
        k    = input['k']
        T0   = input['T0']

        #--------------- v2 page 54, rocket propulsion elements

        m = np.interp(OF, chem.of, chem.m)
        R = 8314.3 # page 50, rocket propulsion elements

        # assumed p2=p3
        v2 = np.sqrt( 2*k/(k-1) * (R*T0 / m) * (1 - (p2/p1)**((k-1)/k)) )

        #--------------- thrust page 36, rocket propulsion elements

        F = mdot * v2

        #--------------- specific impulse

        isp = F / (mdot*n.g0)

        return F, v2, isp, mdot
