from tkinter import *
import imp
import interpolater
import map_objects
import struct

from pylab import *
import numpy as np

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class Header:
	def __init__(self,file):
		self.mag_avg = float(file.readline().split(" ")[0])
		array_size = file.readline()[:-1]
		self.IMAGE_WIDTH = int(array_size)
		self.IMAGE_HEIGHT = int(array_size)
		self.quasar_size = int(file.readline()[:-1])
		self.kappa_gamma = file.readline()[:-1]

def generateMagMap(file,header):
	print("computing magnification map from file")
	image_array_long = np.fromfile(file,np.uint32)
	image_array = np.zeros((header.IMAGE_WIDTH,header.IMAGE_HEIGHT),dtype=(np.str_,7))
	x = header.mag_avg*128
	count = 0
	print(image_array_long[:10])
	print("starting loop")
	for i in np.nditer(image_array_long):
		# pixel = "#%02x%02x%02x" % (color,color,color)
		# image_array[count // header.IMAGE_WIDTH, count % header.IMAGE_HEIGHT] = pixel
		count+=1
	print("done getting mag array")
	magMap = map_objects.ImageMap(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	magMap.setImageArray(image_array)
	return magMap

def generateCanvasArray(width,height,objects):
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

def draw(name,array_size,*objects):
	print("drawing tkinter window and adding objects")
	master = Tk()
	master.wm_title(name)
	canvas_array = generateCanvasArray(array_size[0],array_size[1],objects)
	#interpolate the image to fit inside a reduced size
	interpolated_array = interpolater.interpolate(canvas_array,array_size[0],array_size[1],CANVAS_WIDTH,CANVAS_HEIGHT)
	win = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
	win.pack()
	drawMap(win,interpolated_array,CANVAS_WIDTH,CANVAS_HEIGHT)
	master.mainloop()

def reloadModules():
	imp.reload(interpolater)
	imp.reload(map_objects)

def drawMagMap(headerFile,magMapFile):
	reloadModules()
	#get image from file
	file = open(magMapFile,"rb")
	header = Header(open(headerFile))
	pixel_size = (header.quasar_size * 1.85 * (10**15))/header.IMAGE_WIDTH 
	magMap = generateMagMap(file,header)
	file.close()
	#draw("0924 Image A",[header.IMAGE_WIDTH,header.IMAGE_HEIGHT], magMap)


drawMagMap("0924/Image_A/s90/mapmeta.dat","0924/Image_A/s90/map.bin")
