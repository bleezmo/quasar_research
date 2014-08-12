from tkinter import *
import imp
import map_objects
import struct
import gc

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from scipy import ndimage

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
		file.close()

def plotAndPrint(arr,name):
	colorMap = cm.gray
	colorMap.set_over('white')
	colorMap.set_under('black')
	fig = plt.figure(figsize=(7,7))
	ax = fig.add_axes([0.06, 0.05, 0.6, 0.9])
	ax.imshow(arr,origin="lower",interpolation="bilinear",norm=colors.LogNorm(),cmap=colorMap)
	plt.savefig(name)
	plt.close('all')

def applySobelAndPrint(magArray):
	#apply sobel and print
	sx = ndimage.sobel(magArray, axis=0, mode='constant')
	sy = ndimage.sobel(magArray, axis=1, mode='constant')
	sob = np.hypot(sx, sy)
	plotAndPrint(sob,"sobel_mag_map")

def applyCustomSobelAndPrint(dims,magArray):
	# xmask = [
	# 		[-1,-2,-1],
	# 		[0,0,0],
	# 		[1,2,1]
	# 		]
	# ymask = [
	# 		[-1,0,1],
	# 		[-2,0,2],
	# 		[-1,0,1]
	# 		]

	sobelArray = np.zeros(dims)
	for x in range(1,dims[0]-1):
		for y in range(1,dims[1]-1):
			Gx = (magArray[x-1][y-1]+(2*magArray[x][y-1])+magArray[x+1][y-1])-\
					(magArray[x-1][y+1]+(2*magArray[x][y+1])+magArray[x+1][y+1])
			Gy = (magArray[x+1][y-1]+(2*magArray[x+1][y])+magArray[x+1][y+1])-\
					(magArray[x-1][y-1]+(2*magArray[x-1][y])+magArray[x-1][y+1])
			Gmag = ((Gx**2)+(Gy**2))**.5
			sobelArray[x][y] = Gmag
	sobelArray = sobelArray/np.linalg.norm(sobelArray)

	vectorArr = np.zeros((dims[0]-2,dims[1]-2))
	for x in range(1,dims[0]-1):
		for y in range(1,dims[1]-1):
			if sobelArray[x-1][y-1] < .0003:
				sobelArray[x-1][y-1] = 0.
				vectorArr[x-1][y-1] = 0.
			else:
				Gx = (sobelArray[x-1][y-1]+(2*sobelArray[x][y-1])+sobelArray[x+1][y-1])-\
						(sobelArray[x-1][y+1]+(2*sobelArray[x][y+1])+sobelArray[x+1][y+1])
				Gy = (sobelArray[x+1][y-1]+(2*sobelArray[x+1][y])+sobelArray[x+1][y+1])-\
						(sobelArray[x-1][y-1]+(2*sobelArray[x-1][y])+sobelArray[x-1][y+1])
				angle = np.arctan2(Gy,Gx)
				for i in range(8):
					if ((x+i) < (dims[0]-2)) and ((y+i) < (dims[1]-2)):
						vectorArr[x+i][y+i] = 1

	plotAndPrint(sobelArray,"custom_sobel_mag_map")

def drawSampleMagMap(dims,magArray):
	#get sample array. mag array is to big
	sampleArray = np.zeros(dims)
	for x in range(dims[0]):
		for y in range(dims[1]):
			sampleArray[x][y] = magArray[x,y]
	# plotAndPrint(sampleArray,"mag_map")
	# applySobelAndPrint(sampleArray)
	applyCustomSobelAndPrint(dims,magArray) 

def drawMagMap(headerFile,magMapFile):
	#get image from file
	file = open(magMapFile,"rb")
	header = Header(open(headerFile))
	magArray = np.fromfile(file,np.dtype("i4")).reshape(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	file.close()
	drawSampleMagMap([1400,1400],magArray)

	magArray = None
	gc.collect()

drawMagMap("0924/Image_A/s90/mapmeta.dat","0924/Image_A/s90/map.bin")
