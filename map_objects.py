from imp import reload
import wavelength_mapping
from generic_objects import Circle

reload(wavelength_mapping)
WavelengthMapping = wavelength_mapping.WavelengthMapping
RadiusMapping = wavelength_mapping.RadiusMapping

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
	def __init__(self,center,radius,pixel_size,z=1):
		"""
			center and radius is in pixels
			pixel_size is number of meters that each pixel represents
		"""
		MapObject.__init__(self,z)
		self.centerx = center[0]
		self.centery = center[1]
		self.radius = radius
		self.pixel_size = pixel_size

	def computeAllWavelengths(self,step):
		c = Circle([self.centerx,self.centery],self.radius)
		self.wavelengths = []
		for r in range(step,self.radius+1,step):
			self.wavelengths.append(WavelengthMapping(r,c,self.pixel_size))

	def computeWavelengths(self,wavelengths):
		c = Circle([self.centerx,self.centery],self.radius)
		self.wavelengths = []
		for w in wavelengths:
			self.wavelengths.append(RadiusMapping(w,c,self.pixel_size))

	def applyMagnification(self,mag_array):
		for w in self.wavelengths:
			w.applyMagnification(mag_array)

	def drawPoint(self,x,y,default):
		rhs = self.radius * self.radius
		lhs = ((x - self.centerx)**2)+((y - self.centery)**2)
		#check to see if point is on circle
		if(lhs == rhs):
			return "#%02x%02x%02x" % (255,0,0)
		else:
			return default