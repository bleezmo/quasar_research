import imp
import interpolater
import map_objects
from quasar_data import *

import gc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import random
import os

class Header:
	def __init__(self,file):
		filerm = open(file)
		self.mag_avg = float(filerm.readline().split(" ")[0])
		array_size = filerm.readline()[:-1]
		self.IMAGE_WIDTH = int(array_size)
		self.IMAGE_HEIGHT = int(array_size)
		self.quasar_size = int(filerm.readline()[:-1])
		self.kappa_gamma = filerm.readline()[:-1]
		filerm.close()

def reloadModules():
	imp.reload(interpolater)
	imp.reload(map_objects)

def loadDisk(header, magMapFile,wavelengths,einsteinRadius,diskCenter,diskSize,annulus_removed):
	print("loading magnification map and header file")
	file = open(magMapFile,"rb")
	pixel_size = (header.quasar_size * einsteinRadius)/header.IMAGE_WIDTH
	mag_array = np.fromfile(file,np.dtype("i4")).reshape(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	file.close()
	disk = map_objects.Disk(diskCenter,diskSize,pixel_size)
	print("computing wavelengths in disk")
	stepsize = diskSize//300
	disk.computeWavelengths(wavelengths,smooth_step = stepsize if stepsize > 0 else 1,annulus_removed=annulus_removed)
	print("applying magnification to wavelengths")
	disk.applyMagnification(mag_array)
	return disk

#wavelengths are assumed to be in nanometers
def start(saveDir, headers,magMapFiles,red_shift,wavelengths,einsteinRadius,diskSize,annulus_removed):
	reloadModules()
	shifted_wavelengths = [w/(red_shift+1) for w in wavelengths]
	disk1 = loadDisk(headers[0],magMapFiles[0],shifted_wavelengths,\
		einsteinRadius,diskSize[0][0],diskSize[1],annulus_removed)
	disk2 = loadDisk(headers[1],magMapFiles[1],shifted_wavelengths,\
		einsteinRadius,diskSize[0][1],diskSize[1],annulus_removed)

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

	plt.savefig(saveDir)
	disk1 = None
	disk2 = None
	mag_ratios = None
	plt.close()
	gc.collect()

# headers = (Header("0924/Image_A/s90/mapmeta.dat"),Header("0924/Image_D/s90/mapmeta.dat"))
# magFiles = ("0924/Image_A/s90/map.bin","0924/Image_D/s90/map.bin")
# disk = (((7000,7000),(7000,7000)),600)
# annulus_removed = (100,"inner disk removed")
# start("/home/josh/Desktop/meh2/moremeh",headers,magFiles,q3[0],q3[1],q3[2],disk,annulus_removed)

def automate(countMax):
	#initialization stuff
	gaussian_radius = 600
	headers = (Header("0924/Image_A/s90/mapmeta.dat"),Header("0924/Image_D/s90/mapmeta.dat"))
	magFiles = ("0924/Image_A/s90/map.bin","0924/Image_D/s90/map.bin")
	quasar = q3
	annuli_removed = (None,\
		(100,.1),(100,.2),(100,"inner disk removed"),\
		(200,.1),(200,.2),(200,"inner disk removed"),\
		(400,.1),(400,.2),(400,"inner disk removed")\
		)
	basedir = "/home/josh/Dropbox/MagWavelengthPlots/SDSSJ0924+0219/"

	#automation code to generate the maps
	count = 0
	while count < countMax:
		print("generating maps",count+1,"of",countMax)
		centerx1 = random.randint(gaussian_radius,headers[0].IMAGE_WIDTH-gaussian_radius)
		centery1 = random.randint(gaussian_radius,headers[0].IMAGE_HEIGHT-gaussian_radius)
		centerx2 = random.randint(gaussian_radius,headers[1].IMAGE_WIDTH-gaussian_radius)
		centery2 = random.randint(gaussian_radius,headers[1].IMAGE_HEIGHT-gaussian_radius)
		saveDir = basedir+"center1:"+str(centerx1)+","+str(centery1)+"&"\
						+"center2:"+str(centerx2)+","+str(centery2)+"/"
		os.makedirs(saveDir)
		for i,annulus_removed in enumerate(annuli_removed):
			print("generating map",i+1,"of",len(annuli_removed),"in folder",count+1)
			if annulus_removed == None:
				saveFile = saveDir+"NoAnnulusRemoved"
			elif annulus_removed[1] == "inner disk removed":
				saveFile = saveDir+str(annulus_removed[0])+"nmInnerDiskRemoved"
			else:
				saveFile = saveDir+str(annulus_removed[0])+"nm"+str(int(annulus_removed[1]*100))+"percent"
			start(saveFile, headers, magFiles,\
				quasar[0], quasar[1], quasar[2],\
				(((centerx1,centery1),(centerx2,centery2)),600),\
				annulus_removed
				)
		count+=1

automate(1)