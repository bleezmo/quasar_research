from tkinter import *
import imp
import interpolater
import map_objects

imp.reload(interpolater)
imp.reload(map_objects)

IMAGE_WIDTH = 2048
IMAGE_HEIGHT = 2048
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def getHeader(file):
	print("retrieving headers")
	mag_avg = file.readline()[:-1]
	array_size = file.readline()[:-1]
	quasar_size = file.readline()[:-1]
	kappa_gamma = file.readline()[:-1]
	return (mag_avg,array_size,quasar_size,kappa_gamma)

#this method assumes 'getHeader' has already been called
#and file already points to the image content
def getImage(file):
	print("computing image array from file")
	image_array = []
	largest = 0;
	for row in range(IMAGE_HEIGHT):
		column = []
		for col in range(IMAGE_WIDTH):
			pixel = int(file.readline()[:-1])
			if(largest < pixel):
				largest = pixel
			column.append(pixel)
		image_array.append(column)
	return (largest,image_array)

def generateMagMap(width,height,largest,image,imageMap):
	print("generating normalized magnification image map")
	img_array = []
	for x in range(width):
		col_array = []
		for y in range(height):
			color = (image[x][y]/largest)*256
			col_array.append("#%02x%02x%02x" % (color,color,color))
		img_array.append(col_array)
	imageMap.setImageArray(img_array)

def generateCanvasArray(width,height,*objects):
	print("generating canvas array")
	sorted_objects = sorted(objects,key=lambda o: o.z)
	image_array = []
	for x in range(width):
		col_array = []
		for y in range(height):
			pixelColor = "#%02x%02x%02x" % (255,255,255)
			for o in sorted_objects:
				pixelColor = o.drawPoint(x,y,pixelColor)
			col_array.append(pixelColor)
		image_array.append(col_array)
	return image_array

def drawMap(win,image,width,height):
	print("drawing map")
	for x in range(width):
		for y in range(height):
			win.create_line(x,y,x,y,fill=image[x][y])

def draw(filepath):
	#get image from file
	file = open(filepath)
	header = getHeader(file)
	largest,image = getImage(file)
	file.close()

	#get objects
	magMap = map_objects.ImageMap(IMAGE_WIDTH,IMAGE_HEIGHT)
	generateMagMap(IMAGE_WIDTH,IMAGE_HEIGHT,largest,image,magMap)
	disk = map_objects.Disk([250,250],100)

	master = Tk()
	master.wm_title(filepath)
	canvas_array = generateCanvasArray(IMAGE_WIDTH,IMAGE_HEIGHT,magMap,disk)
	#interpolate the image to fit inside a reduced size
	interpolated_array = interpolater.interpolate(canvas_array,IMAGE_WIDTH,IMAGE_HEIGHT,CANVAS_WIDTH,CANVAS_HEIGHT)
	win = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
	win.pack()
	drawMap(win,interpolated_array,CANVAS_WIDTH,CANVAS_HEIGHT)
	master.mainloop()

draw("image_a_0.dat")