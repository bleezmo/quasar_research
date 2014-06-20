import imp
import interpolater
import map_objects
from quasar_data import *

import gc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

class Header:
	def __init__(self,file):
		self.mag_avg = float(file.readline().split(" ")[0])
		array_size = file.readline()[:-1]
		self.IMAGE_WIDTH = int(array_size)
		self.IMAGE_HEIGHT = int(array_size)
		self.quasar_size = int(file.readline()[:-1])
		self.kappa_gamma = file.readline()[:-1]

def reloadModules():
	imp.reload(interpolater)
	imp.reload(map_objects)

def loadDisk(headerFile, magMapFile,wavelengths,einsteinRadius,diskSize,annulus_removed):
	print("loading magnification map and header file")
	file = open(magMapFile,"rb")
	header = Header(open(headerFile))
	pixel_size = (header.quasar_size * einsteinRadius)/header.IMAGE_WIDTH
	mag_array = np.fromfile(file,np.dtype("i4")).reshape(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	file.close()
	disk = map_objects.Disk(diskSize[0],diskSize[1],pixel_size)
	print("computing wavelengths in disk")
	stepsize = diskSize[1]//150
	disk.computeWavelengths(wavelengths,smooth_step = stepsize if stepsize > 0 else 1,annulus_removed=annulus_removed)
	print("applying magnification to wavelengths")
	disk.applyMagnification(mag_array)
	return disk

#wavelengths are assumed to be in nanometers
def start(headerFiles,magMapFiles,red_shift,wavelengths,einsteinRadius,diskSize,annulus_removed):
	reloadModules()
	shifted_wavelengths = [w/(red_shift+1) for w in wavelengths]
	disk1 = loadDisk(headerFiles[0],magMapFiles[0],shifted_wavelengths,einsteinRadius,diskSize,annulus_removed)
	disk2 = loadDisk(headerFiles[1],magMapFiles[1],shifted_wavelengths,einsteinRadius,diskSize,annulus_removed)

	print("generating plot")
	# plot([w.wavelength for w in disk1.wavelengths],\
	# 	[w.total_magnification for w in disk1.wavelengths],\
	# 	'bo')

	# plot([w.wavelength for w in disk2.wavelengths],\
	# 	[w.total_magnification for w in disk2.wavelengths],\
	# 	'ro')

	mag_ratios = []
	for i in range(len(disk1.wavelengths)):
		mag_ratios.append(disk1.wavelengths[i].total_magnification/disk2.wavelengths[i].total_magnification)

	plt.plot(wavelengths,mag_ratios,'go')
	#adding some text. the offsets are just for positioning
	for i in range(len(wavelengths)):
		plt.text(wavelengths[i],mag_ratios[i]," ({:.3f},{:.3f})".format(wavelengths[i],mag_ratios[i]),fontsize=10)

	plt.show()
	disk1 = None
	disk2 = None
	mag_ratios = None
	gc.collect()

headers = ("0924/Image_A/s90/mapmeta.dat","0924/Image_D/s90/mapmeta.dat")
magFiles = ("0924/Image_A/s90/map.bin","0924/Image_D/s90/map.bin")
diskSize = ([7000,7000],600)
annulus_removed = (100,"inner disk removed")
start(headers,magFiles,q3[0],q3[1],q3[2],diskSize,annulus_removed)
