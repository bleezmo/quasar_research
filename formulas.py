from math import *

#gravitational constant
G_CONSTANT = 6.67/(10**11)
#stefan-boltzmann constant
SB_CONSTANT = 5.67/(10**8)
#Thomson scattering
ST_CONSTANT = 6.65/(10**29)
#speed of light
C_CONSTANT = 3*(10**8)

def ISCO(mbh):
	return (6*G_CONSTANT*mbh)/(C_CONSTANT**2)

def tempOfRadius(mbh,mdot,r):
