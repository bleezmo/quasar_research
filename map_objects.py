class MapObject:
	def __init__(self,z):
		self.z = z
	def drawPoint(self,x,y,default):
		return default

class ImageMap(MapObject):
	def __init__(self,width,height,z=0):
		MapObject.__init__(self,z)
		self.width = width
		self.height = height
	def setImageArray(self,img_array):
		"""
			expects a 2-d array
		"""
		self.img_array = img_array
	def getImageArray(self):
		return self.img_array
	def drawPoint(self,x,y,default):
		if(len(self.img_array) > x and len(self.img_array[x]) > y):
			return self.img_array[x][y]
		else:
			return default

class Disk(MapObject):
	def __init__(self,center,radius,z=1):
		MapObject.__init__(self,z)
		self.centerx = center[0]
		self.centery = center[1]
		self.radius = radius
		self.intensity_mappings = []
		self.computeWavelengths()

	#check to make sure that the given point falls on the circle
	def checkCoord(self,x,y):
		rhs = self.radius * self.radius
		lhs = ((x - self.centerx)**2)+((y - self.centery)**2)
		return lhs <= rhs

	def calculateGaussian(self,x,y):
		xcomponent = ((x - self.centerx)**2)/(2*self.radius**2)
		ycomponent = ((y - self.centery)**2)/(2*self.radius**2)
		color_multiplier = E_CONSTANT**(-(xcomponent+ycomponent))
		return color_multiplier

	def computeWavelengths(self):
		for r in range(self.radius):
			wavelength_max = (B_CONSTANT * (r**(3/4))) / A_CONSTANT
			self.intensity_mappings.append(InstensityMapping(wavelength_max,self.radius))

	def calculateColor(self,x,y):
		color_multiplier = self.calculateGaussian(x,y)
		# max = 255*255*255
		# rfilter = 255<<16
		# bfilter = 255
		# gfilter = 255<<8
		# int_color = int(max * color_multiplier)
		# rcomp = (rfilter & int_color)>>16
		# gcomp = (gfilter & int_color)>>8
		# bcomp = bfilter & int_color
		return "#%02x%02x%02x" % (color_multiplier*255,color_multiplier*255,color_multiplier*255)

	def drawPoint(self,x,y,default):
		if(self.checkCoord(x,y)):

			return self.calculateColor(x,y)
		else:
			return default