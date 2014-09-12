from imp import reload
from generic_objects import Circle

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

	def computeAllWavelengths(self,WavelengthMapping,step=1,annulus_removed=None):
		c = Circle([self.centerx,self.centery],self.radius)
		self.wavelengths = []
		for r in range(1,self.radius+step,step):
			self.wavelengths.append(WavelengthMapping(r,c,self.pixel_size,annulus_removed = annulus_removed,smooth_step = step))

	def computeWavelengths(self,RadiusMapping,wavelengths,smooth_step = 1,annulus_removed = None):
		c = Circle([self.centerx,self.centery],self.radius)
		self.wavelengths = []
		for w in wavelengths:
			self.wavelengths.append(RadiusMapping(w,c,self.pixel_size,smooth_step = smooth_step, annulus_removed = annulus_removed))

	def applyMagnification(self,mag_array):
		tempArray = []
		for w in self.wavelengths:
			w.applyMagnification(mag_array)
			# if there are empty wavelengths (no computed magnification) then remove from list
			# this can happen if the radius peak chosen is within ISCO
			if(w.total_magnification != 0):
				tempArray.append(w)
		self.wavelengths = tempArray



	def drawPoint(self,x,y,default):
		rhs = self.radius * self.radius
		lhs = ((x - self.centerx)**2)+((y - self.centery)**2)
		#check to see if point is on circle
		if(lhs == rhs):
			return "#%02x%02x%02x" % (255,0,0)
		else:
			return default