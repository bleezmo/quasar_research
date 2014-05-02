from generic_objects import *

#mass of black hole
MBH = 1000000000
EDDINGTON_RATIO = 0.1
#euler's constant
E_CONSTANT = 2.718281828
#wein's displacement constant
B_CONSTANT = .002898
#part of wavelength formula T(r)=A*r^(-3/4)
A_CONSTANT = ((3.940881993343145/(10**24))*(MBH**2)*EDDINGTON_RATIO)**0.25

class WavelengthMapping:
	def __init__(self,radius_peak,disk):
		self.radius_peak = radius_peak
		self.max_radius = disk.radius
		self.centerx = disk.center[0]
		self.centery = disk.center[1]
		self.wavelength = (B_CONSTANT * (radius_peak**(3/4))) / A_CONSTANT
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



