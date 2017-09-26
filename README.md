# PyBurn

A Hybrid Rocket Motor Propulsion Model - Python

+ Combust.py : The primary run script, where all experimental / geometrical parameters are input
+ Thermo.py : Thermodynamical + some thermochemical calculations to determine combustion parameters
+ Nozzle.py : Isentropic flow through nozzles based on [5]. Determines thrust and efficiencies
+ Properties.py : Approximations of key thermochemical variables with respect to oxidizer/fuel ratio. Taken from [2], Fig 4
+ Inject.py : An orifice-plate model based injector flow rate calculator

Currently, only supports analysis of ABS/N2O rocket motors.

To run, call `python Combust.py`

# References

0. http://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1079&context=mae_facpub
1. http://www.d.umn.edu/~rrosandi/Hybrids/Reports/Numerical_Model.pdf
2. http://www.enu.kz/repository/2011/AIAA-2011-5909.pdf
3. https://www.fire.tc.faa.gov/pdf/05-14.pdf
4. https://goo.gl/1Eh1Gf
5. Rocket Propulsion Elements, Sutton: https://goo.gl/kCFbHc
