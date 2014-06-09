from tkinter import *
import imp
import interpolater
import map_objects
import struct
import gc

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

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

def drawMagMap(headerFile,magMapFile):
	#get image from file
	file = open(magMapFile,"rb")
	header = Header(open(headerFile))
	magArray = np.fromfile(file,np.dtype("i4")).reshape(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	file.close()
	colorMap = cm.gray
	colorMap.set_over('white')
	colorMap.set_under('black')
	plt.imshow(magArray,origin="lower",interpolation="bilinear",norm=colors.Normalize(),cmap=colorMap)
	plt.show()
	magArray = None
	gc.collect()

drawMagMap("0924/Image_A/s90/mapmeta.dat","0924/Image_A/s90/map.bin")