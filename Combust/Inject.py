"""
    Inputs:

        - Orifice diameter (d)
        - Experimental data:
            - Flow velocity (v)
            - Input pressure (p)

    Outputs:

        - Water mass flow rate
        - Volumetric flow rate
        - Nitrous mass flow rate

    Based on: https://en.wikipedia.org/wiki/Orifice_plate

"""


# NOTE THAT ALL OF THIS IS DEPRECATED IN FAVOR OF EXPERIMENTAL DATA, FOR NOW

import numpy as np

def evaluate(run):
    # vol. flow rate, kg/(sec * m**3)
    # mass flow rate, kg/sec

    qv = run['Cd'] / np.sqrt( 1 - ( run['d'] / run['D'] )**4 ) # first term
    qv = qv * 1 * np.pi * run['d']**2                    # area and epsilon
    qv = qv * np.sqrt( 2*run['dP']/run['rho'] )     # pressure contribution

    qm = run['rho']*qv # mass flow rate

    return qv,qm

injector = {
        'rho': 1000,     # kg/m**3 WATER
        'Cd' : 0.82,      # discharge coefficient
        'D'  : 3.175e-3, # pipe diameter, m
        'd'  : 1.5e-3,   # hole diameter, m
        'dP' : 172e3     # delta pressure
      }

N2O_rho = 1.98      # kg/m**3 N2O GAS
#N2O_rho = 772.25012 # kg/m**3 N2O LIQUID

qv, qm_H2O = evaluate(injector)
