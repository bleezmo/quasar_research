class Disk:
	def __init__(self,center,radius):
		self.centerx = center[0]
		self.centery = center[1]
		self.radius = radius

	#check to make sure that the given point falls on the circle
	def checkCoord(self,x,y):
		rhs = self.radius * self.radius
		lhs = ((x - self.centerx)**2)+((y - self.centery)**2)
		return lhs <= rhs

	#return the color of the circle at the point if the point falls on the circle
	#otherwise, return the background color given
	def getCircleColor(self,x,y,bg_color):
		if(self.checkCoord(x,y)):
			return "#%02x%02x%02x" % (255,0,0)
		else:
			return bg_color