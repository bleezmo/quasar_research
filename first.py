from tkinter import *
import imp
import interpolater
import map_objects

from pylab import *

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class Header:
	def __init__(self,file):
		self.mag_avg = file.readline()[:-1]
		array_size = file.readline()[:-1][1:].split(" ")
		self.IMAGE_WIDTH = int(array_size[0])
		self.IMAGE_HEIGHT = int(array_size[1])
		self.quasar_size = file.readline()[:-1]
		self.quasar_size = int(''.join([c for c in self.quasar_size if c in '1234567890']))
		self.kappa_gamma = file.readline()[:-1]


class MagnificationArray:
	#this method assumes 'getHeader' has already been called
	#and file already points to the image content
	def __init__(self,file,header):
		print("computing image array from file")
		image_array = []
		largest = 0
		for row in range(header.IMAGE_HEIGHT):
			column = []
			for col in range(header.IMAGE_WIDTH):
				pixel = int(file.readline()[:-1])
				if(largest < pixel):
					largest = pixel
				column.append(pixel)
			image_array.append(column)
		self.array = image_array
		self.largest = largest

def generateMagMap(width,height,mag_array):
	print("generating normalized magnification image map")
	img_array = []
	for x in range(width):
		col_array = []
		for y in range(height):
			color = (mag_array.array[x][y]/mag_array.largest)*256
			col_array.append("#%02x%02x%02x" % (color,color,color))
		img_array.append(col_array)
	magMap = map_objects.ImageMap(width,height)
	magMap.setImageArray(img_array)
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

#wavelengths are assumed to be in nanometers
def start(red_shift,wavelengths):
	reloadModules()
	wavelengths = [w/(red_shift+1) for w in wavelengths]
	#get image from file
	file = open("image_a_0.dat")
	header = Header(file)
	pixel_size = (header.quasar_size * 1.85 * (10**15))/header.IMAGE_WIDTH 
	mag_arraya = MagnificationArray(file,header)
	file.close()
	file = open("image_b_0.dat")
	header = Header(file)
	mag_arrayb = MagnificationArray(file,header)
	file.close()

	#get objects
	diska = map_objects.Disk([250,250],200,pixel_size)
	print("computing wavelengths in disk")
	diska.computeWavelengths(wavelengths,annulus_removed=(100,.2))
	print("applying magnification to wavelengths")
	diska.applyMagnification(mag_arraya.array)

	diskb = map_objects.Disk([250,250],200,pixel_size)
	print("computing wavelengths in disk")
	diskb.computeWavelengths(wavelengths,annulus_removed=(100,.2))
	print("applying magnification to wavelengths")
	diskb.applyMagnification(mag_arrayb.array)

	# plot([w.wavelength for w in diska.wavelengths],\
	# 	[w.total_magnification for w in diska.wavelengths],\
	# 	'bo')

	# plot([w.wavelength for w in diskb.wavelengths],\
	# 	[w.total_magnification for w in diskb.wavelengths],\
	# 	'ro')

	mag_ratios = []
	for i in range(len(diska.wavelengths)):
		mag_ratios.append(diska.wavelengths[i].total_magnification/diskb.wavelengths[i].total_magnification)

	plot([w.wavelength for w in diska.wavelengths],mag_ratios,'go')

	# Set x limits
	#xlim(0,int(disk.wavelengths[-1:][0].wavelength)+10)

	show()

	# draw("image_a_0.dat",[header.IMAGE_WIDTH,header.IMAGE_HEIGHT], generateMagMap(header.IMAGE_WIDTH,header.IMAGE_HEIGHT,mag_array), disk)

# MGJ0414+0534 (rs=2.64)wavelengths(nm):
# WFC3/UVIS Imaging F467M - 468.3
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
q1=(2.64,(468.3,621.9,761.2,843.6,1248.6))

#RXJ0911+0551 (rs=2.80)wavelengths(nm):
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F689M - 687.6
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q2=(2.8,(544.7,621.9,687.6,843.6,1248.6,1536.9))

#SDSSJ0924+0219 (rs=1.524) wavelengths(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F105W - 1055.2
# WFC3/IR Imaging F160W - 1536.9
q3=(1.524,(410.9,544.7,621.9,843.6,1055.2,1536.9))

# PG1115+080 (rs=1.72) wavelengths(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
# WFC3/IR Imaging F105W - 1055.2
q4=(1.72,(410.9,621.9,843.6,1248.6,1536.9,1055.2))

# B1422+231 (rs=3.62) wavelengths(nm):
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
# WFC3/IR Imaging F105W - 1055.2
q5=(3.62,(621.9,761.2,843.6,1248.6,1536.9,1055.2))

# WFIJ2026-4536 (rs=2.23)wavelength(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F689M - 687.6
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F105W - 1055.2
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q6=(2.23,(410.9,544.7,687.6,761.2,843.6,1055.2,1248.6,1536.9))

# WFIJ2033-4723 (rs=1.66) wavelengths(nm):
# WFC3/UVIS Imaging F467M - 468.3
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F814W - 802.4
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q7=(1.66,(468.3,621.9,761.2,802.4,1248.6,1536.9))

start(q3[0],q3[1])