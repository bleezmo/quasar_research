from tkinter import *
import imp
import interpolater
import acc_disk

imp.reload(interpolater)
imp.reload(acc_disk)

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

def drawMap(win,image,largest,width,height):
	print("drawing map")
	for x in range(width):
		for y in range(height):
			color = (image[x][y]/largest)*256
			ptcolor = "#%02x%02x%02x" % (color,color,color)
			win.create_line(x,y,x,y,fill=ptcolor)

def draw(filepath):

	file = open(filepath)
	header = getHeader(file)
	largest,image = getImage(file)
	file.close()
	#interpolate the image to fit inside a reduced size
	interpolated_image = interpolater.interpolate(image,IMAGE_WIDTH,IMAGE_HEIGHT,CANVAS_WIDTH,CANVAS_HEIGHT)
	master = Tk()
	master.wm_title(filepath)
	win = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
	win.pack()
	drawMap(win,interpolated_image,largest,CANVAS_WIDTH,CANVAS_HEIGHT)
	master.mainloop()

def drawDisk(win,disk,width,height):
	bg_color = "#%02x%02x%02x" % (255,255,255)
	for x in range(width):
		for y in range(height):
			color = disk.getCircleColor(x,y,bg_color)
			win.create_line(x,y,x,y,fill=color)

def drawCircleTest():
	master = Tk()
	master.wm_title("blah blah")
	win = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
	win.pack()
	disk = acc_disk.Disk([50,50],20)
	drawDisk(win,disk,CANVAS_WIDTH,CANVAS_HEIGHT)
	master.mainloop()

#draw("image_a_0.dat")
drawCircleTest()