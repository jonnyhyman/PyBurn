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
# ----------------------------------------------------- Thermochemical Analysis
class Thermo(object):

    def __init__(t):

        # constants, adjusted from english -> metric (pg. 602, rocket prop.)
        #t.C0 = 0.036
        #t.C1 = 0.8
        #t.C2 = 0.23

        t.C0 = 0.047
        t.C1 = 4/5
        t.C2 = 0.153
        t.C3 = 1/5
        t.C4 = 0.23

        t.SLP = 101325       # pascals, 1 atm
        t.hv  = 2.3*1e3*1e3  # heat of vaporization,  kJ/g [3] -> J/kg
        t.cp  = 1674.72      # [4], converted units to J/kgK
        t.Tfuel  = 734.15    # [3], Table A-1, Tp, converted units to K

    def evaluate(t,input):
        """ Thermochemical analysis at a fixed time-slice """

        OF = input['OF']

        Pr  = np.interp(OF, chem.of, chem.Pr)
        mu  = np.interp(OF, chem.of, chem.mu)
        T0  = np.interp(OF, chem.of, chem.T0)
        k   = np.interp(OF, chem.of, chem.k)

        thermo = {}

        rho_o  = input['rho_o']
        rho_f  = input['rho_f']
        Ac     = input['Ac']
        L      = input['L']
        p0     = input['p0']          # ox feed pressure
        p1     = input['p1_t']        # chamber pressure
        mdot_o = input['v_dot']*rho_o # kg / sec

        #$ freestream propellant mass flow rate
        G = (input['A_ox']*input['Cd_ox'] / Ac) * np.sqrt(2*rho_o*(p0 - p1))

        #$ nondimensional fuel mass flux / blowing coefficient
        B = t.cp * (T0-t.Tfuel) / t.hv

        #$ page 602, rocket propulsion elements
        #$ and page 19, reference 2:
        #$ units = m3/kg * (kg/m2s)*1/5 * (kg/m2s)*4/5 = m/s
        regression = t.C0*(G**t.C1)/(rho_f*Pr**t.C2)*(mu/L)**(t.C3)*(B**t.C4)

        mdot_f = input['A_burn'] * rho_f * regression  # m2*kg/m3*m/s = kg/s

        # determine what the "modeled" OF is. Seems to trend higher than truth
        OF = mdot_o / mdot_f

        thermo['mdot'] = mdot_o + mdot_f
        thermo['At']   = input['At']
        thermo['OF']   = OF
        thermo['k']    = k # specific heat ratio

        # assume stagnation pressure = chamber pressure, page 53
        thermo['p1'] = p1
        thermo['p3'] = input['p3']
        thermo['T0'] = T0

        return thermo
