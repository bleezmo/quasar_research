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

def start():
	reloadModules()
	#get image from file
	file = open("image_a_0.dat")
	header = Header(file)
	mag_arraya = MagnificationArray(file,header)
	file.close()
	file = open("image_b_0.dat")
	header = Header(file)
	mag_arrayb = MagnificationArray(file,header)
	file.close()

	#get objects
	diska = map_objects.Disk([250,250],100)
	print("computing wavelengths in disk")
	diska.computeWavelengths(1)
	print("applying magnification to wavelengths")
	diska.applyMagnification(mag_arraya.array)

	diskb = map_objects.Disk([250,250],100)
	print("computing wavelengths in disk")
	diskb.computeWavelengths(1)
	print("applying magnification to wavelengths")
	diskb.applyMagnification(mag_arrayb.array)

	plot([w.wavelength for w in diska.wavelengths],\
		[w.total_magnification for w in diska.wavelengths],\
		'bo')

	plot([w.wavelength for w in diskb.wavelengths],\
		[w.total_magnification for w in diskb.wavelengths],\
		'ro')

	# Set x limits
	xlim(0,int(disk.wavelengths[-1:][0].wavelength)+10)

	show()

	# draw("image_a_0.dat",[header.IMAGE_WIDTH,header.IMAGE_HEIGHT], generateMagMap(header.IMAGE_WIDTH,header.IMAGE_HEIGHT,mag_array), disk)

def graph_tut():

	# Create a new figure of size 8x6 points, using 80 dots per inch
	figure(figsize=(8,6), dpi=80)

	# Create a new subplot from a grid of 1x1
	subplot(1,1,1)

	X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
	C,S = np.cos(X), np.sin(X)

	print(C[0])

	# Plot cosine using blue color with a continuous line of width 1 (pixels)
	plot(X, C, color="blue", linewidth=1.0, linestyle="-")

	# Plot sine using green color with a continuous line of width 1 (pixels)
	plot(X, S, color="green", linewidth=1.0, linestyle="-")

	# Set x limits
	xlim(-4.0,4.0)

	# Set x ticks
	xticks(np.linspace(-4,4,9,endpoint=True))

	# Set y limits
	ylim(-1.0,1.0)

	# Set y ticks
	yticks(np.linspace(-1,1,5,endpoint=True))

	# Save figure using 72 dots per inch
	# savefig("exercice_2.png",dpi=72)

	# Show result on screen
	show()

start()