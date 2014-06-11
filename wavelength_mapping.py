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
#part of wavelength formula wavelength = (B_CONSTANT/A_CONSTANT)*r^(3/4)
BA_CONSTANT = B_CONSTANT/A_CONSTANT

class WavelengthMapping:
	def __init__(self,radius_peak,disk,pixel_size,wavelength = -1,annulus_removed = None,smooth_step = 1):
		"""
			radius_peak the particular annulus we are calculating the wavelength for
			disk has a bunch of stuff we need
			wavelength is stored in nanometers
			annulus_removed - percentage (between 0 and 1) of radius_peak to remove from calculation
		"""
		self.radius_peak = radius_peak
		self.max_radius = disk.radius
		self.centerx = disk.center[0]
		self.centery = disk.center[1]
		self.radius_peak_meters = self.radius_peak*pixel_size
		if annulus_removed != None:
			annulus = (((A_CONSTANT*(annulus_removed[0]/1000000000))/B_CONSTANT)**(4/3))/pixel_size
			width = annulus*annulus_removed[1]
			self.width_removed = (annulus-(width/2),annulus+(width/2))
		else:
			self.width_removed = None
		#calculate the wavelength in nanometers
		if(wavelength == -1):
			self.wavelength = (BA_CONSTANT * (self.radius_peak_meters**(3/4)))*1000000000
		else:
			self.wavelength = wavelength
		self.computeAndNormalizeIntensityPoints(smooth_step)

	def calculateGaussian(self,x,y):
		xcomponent = ((x-self.centerx)**2)/(2*self.radius_peak**2)
		ycomponent = ((y-self.centery)**2)/(2*self.radius_peak**2)
		multiplier = E_CONSTANT**(-(xcomponent+ycomponent))
		return multiplier

	#compute the intensity based on the gaussian.
	def computeAndNormalizeIntensityPoints(self,smooth_step):
		self.intensity_points = []
		self.total_intensity = 0
		def computeIntensityPoint(x,y):
			g = self.calculateGaussian(x,y)
			ip = Point(x,y,g)
			self.total_intensity = self.total_intensity + g
			return ip
		for x in range(smooth_step,self.max_radius+smooth_step,smooth_step):
			for y in range(smooth_step,self.max_radius+smooth_step,smooth_step):
				radius = ((x**2)+(y**2))**.5
				isInsideDisk = radius <= self.max_radius
				inRemovedAnnulus = (self.width_removed != None) and \
									(radius >= self.width_removed[0]) and \
									(radius <= self.width_removed[1])
				if(isInsideDisk and not inRemovedAnnulus):
					self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery+y))
					self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery+y))
					self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery-y))
					self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery-y))
				elif(isInsideDisk):
					self.intensity_points.append(Point(self.centerx+x,self.centery+y,0))
					self.intensity_points.append(Point(self.centerx-x,self.centery+y,0))
					self.intensity_points.append(Point(self.centerx+x,self.centery-y,0))
					self.intensity_points.append(Point(self.centerx-x,self.centery-y,0))
		for pt in self.intensity_points:
			pt.value = pt.value / self.total_intensity

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

class RadiusMapping(WavelengthMapping):
	"""
	here we assume that the given wavelength is given in nanometers
	"""
	def __init__(self,wavelength,disk,pixel_size,smooth_step = 1,annulus_removed = None):
		radius_peak = (((A_CONSTANT*(wavelength/1000000000))/B_CONSTANT)**(4/3))/pixel_size
		WavelengthMapping.__init__(self,radius_peak,disk,pixel_size,wavelength,smooth_step = smooth_step,annulus_removed = annulus_removed)


