class IntensityMultiplierPoint:
	def __init__(self,x,y,intensity_multiplier):
		self.x = x
		self.y = y
		self.intensity_multiplier = intensity_multiplier

E_CONSTANT = 2.718281828
B_CONSTANT = 1
A_CONSTANT = 1

class WavelengthMapping:
	def __init__(self,center,radius):
		self.radius = radius
		self.center
		self.intensity_multiplier_points = computeIntensityMultiplierPoints()

	def calculateGaussian(self,x,y):
		xcomponent = ((x - self.centerx)**2)/(2*self.radius**2)
		ycomponent = ((y - self.centery)**2)/(2*self.radius**2)
		multiplier = E_CONSTANT**(-(xcomponent+ycomponent))
		return multiplier

	def computeIntensityMultiplierPoint(self,x,y):
		return IntensityMultiplierPoint(x,y,self.caclulateGaussian(x,y))
	def computeIntensityMultiplierPoints(self):
		points = []
		for x in range(self.radius):
			for y in range(self.radius):
				points.append(computeIntensityMultiplierPoint(self.centerx+x,self.centery+y))
				points.append(computeIntensityMultiplierPoint(self.centerx-x,self.centery+y))
				points.append(computeIntensityMultiplierPoint(self.centerx+x,self.centery-y))
				points.append(computeIntensityMultiplierPoint(self.centerx-x,self.centery-y))

class IntensityMapping:
	def __init__(self,wavelength):
		self.wavelength = wavelength


