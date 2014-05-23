from generic_objects import *
from math import pi

#mass of black hole (kg)
MBH = 1.989*(10**39)
#ratio of emitted light over max emitting light
EDDINGTON_RATIO = 0.1
#wein's displacement constant (m*K)
B_CONSTANT = 2.898/(10**3)
#euler's constant
E_CONSTANT = 2.718281828
#mass of proton (kg)
PROTON_MASS = 1.673/(10**27) 
#speed of light (m/s)
C_CONSTANT = 3*(10**8)
#thomson scattering cross section (m^2)
SIGMAT = 6.65/(10**29)
#gravitational constant
G_CONSTANT = 6.67/(10**11)
#stefan-boltzmann constant
SB_CONSTANT = 5.67/(10**8)
#mass accretion rate through an annulus of disk
MDOT = (48*G_CONSTANT*MBH*PROTON_MASS*pi*EDDINGTON_RATIO)/(C_CONSTANT*SIGMAT)
#part of temperature profile of accretion disk T(r)=A*r^(-3/4)
A_CONSTANT = ((G_CONSTANT*MBH*MDOT)/(8*pi*SB_CONSTANT))**.25
#part of wavelength formula wavelength = (B_CONSTANT/A_CONSTANT)*r^(-3/4)
BA_CONSTANT = B_CONSTANT/A_CONSTANT


class WavelengthMapping:
	def __init__(self,radius_peak,disk,pixel_size):
		"""
			radius_peak the particular annulus we are calculating the wavelength for
			disk has a bunch of stuff we need
		"""
		self.radius_peak = radius_peak
		self.max_radius = disk.radius
		self.centerx = disk.center[0]
		self.centery = disk.center[1]
		self.radius_peak_meters = self.radius_peak*pixel_size
		self.wavelength = BA_CONSTANT * (self.radius_peak_meters**(3/4))
		self.computeAndNormalizeIntensityPoints()

	def calculateGaussian(self,x,y):
		xcomponent = ((x-self.centerx)**2)/(2*self.radius_peak**2)
		ycomponent = ((y-self.centery)**2)/(2*self.radius_peak**2)
		multiplier = E_CONSTANT**(-(xcomponent+ycomponent))
		return multiplier

	#compute the intensity based on the gaussian.
	def computeAndNormalizeIntensityPoints(self):
		self.intensity_points = []
		self.total_intensity = 0
		def computeIntensityPoint(x,y):
			g = self.calculateGaussian(x,y)
			ip = Point(x,y,g)
			self.total_intensity = self.total_intensity + g
			return ip
		for x in range(self.max_radius):
			for y in range(self.max_radius):
				self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery+y))
				self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery+y))
				self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery-y))
				self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery-y))
		for pt in self.intensity_points:
			pt.value = pt.value / self.total_intensity

	def checkCoord(self,x,y):
		rhs = self.radius * self.radius
		lhs = ((x - self.centerx)**2)+((y - self.centery)**2)
		return lhs <= rhs

	def applyMagnification(self,mag_array):
		"""
			apply magnification to the intensity points. be sure to call computeIntensityPoints first
		"""
		self.total_magnification = 0
		self.mag_points = []
		for pt in self.intensity_points:
			mag_point = Point(pt.x,pt.y,mag_array[pt.x][pt.y]*pt.value)
			self.mag_points.append(mag_point)
			self.total_magnification = self.total_magnification + mag_point.value



