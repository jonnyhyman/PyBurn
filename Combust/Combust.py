"""

    Written by Jonny Hyman, 2017
    www.jonnyhyman.com

    Ref 0 http://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1079&context=mae_facpub
    Ref 1 http://www.d.umn.edu/~rrosandi/Hybrids/Reports/Numerical_Model.pdf
    Ref 2 http://www.enu.kz/repository/2011/AIAA-2011-5909.pdf
    Ref 3 https://www.fire.tc.faa.gov/pdf/05-14.pdf
    Ref 4 https://goo.gl/1Eh1Gf

    Rocket Propulsion Elements, https://goo.gl/kCFbHc

    This combustion model, given geometric and environmental inputs gives
        - Thrust, V2, ISP, Mass Flow, and other properties for ABS/N2O hybrids

    The caveat is that the INPUTs include:
        - Target chamber pressure
        - Target oxidizer/fuel ratio, both of which vary continuously, and are
                                      dependent on the output variables

    Given experimental data from 0, we observe that:
    - Efficiency is somewhat "over-estimated". Actual / Pred. ISP = 200s / 238s
    - Regression model holds some error, as seen by the fact that the O / F
        ratio input to the model does not equal the output O / F calculated
        by the regression model, when against test data

    Also, note that this is a steady-state / "startup" analysis, no provisions
    have been made yet to calculate dynamic behavior.

    Program execution is roughly:
        x = Injector()
        y includes x
        z = Thermo(y)
        show Nozzle(z)
"""

import numpy as np

from Thermo import Thermo
from Nozzle import Nozzle

thermo = Thermo()
nozzle = Nozzle()

parameters = {
                'v_dot'   : 0,             # m3/sec, tuned for O / F ratio
                'rho_f'   : 975,           # kg/m3, fuel density
                'rho_o'   : 1.98,          # kg/m3, oxidizer density
                'p0'      : 345*1e3*1.3,   # pascals, oxidizer feed pressure
                'p1_t'    : 333*1e3,       # pascals, chamber pressure target
                'p3'      : 95380,         # pascals, atmospheric pressure
                'R'       : 0.010,         # meters, port diameter
                'Rt'      : 0.010,         # meters, throat diameter
                'L'       : 0.095,         # meters

                # Injector parameters
                'd'       : 1.5e-3,        # meters, injector orifice size
                'Cd_ox'   : 0.82,          # injector discharge coefficient
             }

# A_burn is the fuel grain surface area being burned
parameters['A_burn'] = (2 * np.pi * parameters['R']) * parameters['L']
parameters['At']     = np.pi * (parameters['Rt'])**2  # throat area
parameters['Ac']     = np.pi * (parameters['R'])**2  # fuel xsctn chamber area
parameters['A_ox']   = np.pi * parameters['d']**2   # effective oxidizer area

# Drives the entire shebang. Tune for desired thrust
parameters['OF'] = 5.5

if __name__ == '__main__':

    # Tune vdot until desired ox/fuel ratio is approximately met (within ~0.01)
    while abs(parameters['OF'] - thermo.evaluate(parameters)['OF']) > 0.01:

        difference = abs(parameters['OF'] - thermo.evaluate(parameters)['OF'])

        # proportional descent, may be gradient descent in the future
        parameters['v_dot'] += .0001*difference

        print("finding vdot ... O/F error:", '{:.02f}'.format(difference) )

    therm = thermo.evaluate(parameters)
    F, v2, isp, mdot = nozzle.evaluate(therm)

    print()
    print('  Thrust: ', F, 'N')
    print('  v2    : ', v2, 'm/s')
    print('  ISP   : ', isp, 'sec')
    print('  M Dot : ', mdot, 'kg/s')
    print('  P1    : ', therm['p1']*1e-3, 'kPa')
    print('  P1/P3 : ', therm['p1']/therm['p3'])
    print('  O / F : ', parameters['OF'],'=>',therm['OF'])
    print('  T0    : ', therm['T0'], 'K')
    print('  R Dot : ', thermo.regression*1e3, 'mm/s')
    print()
    print('  REQUIREMENTS')
    print('  V Dot     : ', parameters['v_dot'], 'm3/s')
    print('  M Dot Ox  :', thermo.mdot_o, 'kg/s')
    print('  M Dot H2O : ', parameters['v_dot']*1000, 'kg/s')

    # M Dot H2O represents the equivalent water mass flow rate at
    #  equivalent feed / "top" pressure
