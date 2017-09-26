"""
    NOTE:
    Utilize as a standalone calculator for injector - not tied to Combust.py

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
import numpy as np

def evaluate(run):
    # vol. flow rate, kg/(sec * m**3)
    # mass flow rate, kg/sec

    qv = run['Cd'] / np.sqrt( 1 - ( run['d'] / run['D'] )**4 ) # first term
    qv = qv * 1 * np.pi * run['d']**2                    # area and epsilon
    qv = qv * np.sqrt( 2*run['dP']/run['rho'] )     # pressure contribution

    qm = run['rho']*qv  # mass flow rate

    return qv,qm

injector = {
        'rho': 1000,     # kg/m**3 WATER
        'D'  : 3.175e-3, # pipe diameter, m
        'd'  : 1.5e-3,   # hole diameter, m
        'dP' : 172e3,    # delta pressure, Pa
        'Cd' : 0.82,     # discharge coefficient, fit to measured dm/dt
        'md' : 1.3,      # kg/s
      }
