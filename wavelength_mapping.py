from generic_objects import *

E_CONSTANT = 2.718281828
B_CONSTANT = 1
A_CONSTANT = 1

class WavelengthMapping:
	def __init__(self,radius_peak,disk):
		self.radius_peak = radius_peak
		self.max_radius = disk.radius
		self.centerx = disk.center[0]
		self.centery = disk.center[1]
		self.wavelength = (B_CONSTANT * (radius_peak**(3/4))) / A_CONSTANT
		self.computeIntensityPoints()

	def calculateGaussian(self,x,y):
		xcomponent = ((x-self.centerx)**2)/(2*self.radius_peak**2)
		ycomponent = ((y-self.centery)**2)/(2*self.radius_peak**2)
		multiplier = E_CONSTANT**(-(xcomponent+ycomponent))
		return multiplier

	#compute the intensity based on the gaussian.
	def computeIntensityPoints(self):
		self.intensity_points = []
		def computeIntensityPoint(x,y):
			ip = Point(x,y,self.calculateGaussian(x,y))
			return ip
		for x in range(self.max_radius):
			for y in range(self.max_radius):
				self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery+y))
				self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery+y))
				self.intensity_points.append(computeIntensityPoint(self.centerx+x,self.centery-y))
				self.intensity_points.append(computeIntensityPoint(self.centerx-x,self.centery-y))

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



