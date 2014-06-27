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

class DiskDetails:
	def __init__(self,red_shift,wavelengths,einsteinRadius,diskSize,annulus_removed):
		self.red_shift = red_shift
		self.wavelengths = wavelengths
		self.einsteinRadius = einsteinRadius
		self.diskSize = diskSize
		self.annulus_removed = annulus_removed

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
def plot(axis, maplegend, headers,magMapFiles,diskDetails):
	reloadModules()
	shifted_wavelengths = [w/(diskDetails.red_shift+1) for w in diskDetails.wavelengths]
	disk1 = loadDisk(headers[0],magMapFiles[0],shifted_wavelengths,\
		diskDetails.einsteinRadius,diskDetails.diskSize[0][0],diskDetails.diskSize[1],diskDetails.annulus_removed)
	disk2 = loadDisk(headers[1],magMapFiles[1],shifted_wavelengths,\
		diskDetails.einsteinRadius,diskDetails.diskSize[0][1],diskDetails.diskSize[1],diskDetails.annulus_removed)

	print("generating plot")

	mag_ratios = []
	for i in range(len(disk1.wavelengths)):
		mag_ratios.append(disk1.wavelengths[i].total_magnification/disk2.wavelengths[i].total_magnification)
	
	if maplegend == None:
		axis.plot(diskDetails.wavelengths,mag_ratios,'go-')
	else:
		axis.plot(diskDetails.wavelengths,mag_ratios,maplegend[0],label=maplegend[1])
	#adding some text. the offsets are just for positioning
	for i in range(len(diskDetails.wavelengths)):
		axis.text(diskDetails.wavelengths[i],mag_ratios[i]," ({:.2f},{:.2f})".format(diskDetails.wavelengths[i],mag_ratios[i]),fontsize=10)

	axis.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	disk1 = None
	disk2 = None
	mag_ratios = None

def start(headers,magFiles,diskDetails):
	fig = plt.figure(figsize=(13,7))
	ax = fig.add_axes([0.06, 0.05, 0.6, 0.9])
	plot(ax,("ko-","no annulus removed"),headers,magFiles,diskDetails)
	plt.show()
	plt.close('all')
# headers = (Header("0924/Image_A/s90/mapmeta.dat"),Header("0924/Image_D/s90/mapmeta.dat"))
# magFiles = ("0924/Image_A/s90/map.bin","0924/Image_D/s90/map.bin")
# disk = (((7000,7000),(7000,7000)),100)
# annulus_removed = None
# diskDetails = DiskDetails(q3[0],q3[1],q3[2],disk,annulus_removed)
# start(headers,magFiles,diskDetails)

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
	maplegend = (("ko-","no annulus removed"),\
		("go-","10% annulus removed at 100nm"),("gD--","20% annulus removed at 100nm"),("gs:","Inner disk removed from 100nm"),\
		("ro-","10% annulus removed at 200nm"),("rD--","20% annulus removed at 200nm"),("rs:","Inner disk removed from 200nm"),\
		("bo-","10% annulus removed at 400nm"),("bD--","20% annulus removed at 400nm"),("bs:","Inner disk removed from 400nm"),\
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
						+"center2:"+str(centerx2)+","+str(centery2)
		fig = plt.figure(figsize=(12,7))
		ax = fig.add_axes([0.06, 0.05, 0.6, 0.9])
		for i,annulus_removed in enumerate(annuli_removed):
			print("generating map",i+1,"of",len(annuli_removed),"in folder",count+1)
			diskDetails = DiskDetails(quasar[0], quasar[1], quasar[2],\
						(((centerx1,centery1),(centerx2,centery2)),600),\
						annulus_removed)
			plot(ax,maplegend[i],headers, magFiles,diskDetails)
		plt.savefig(saveDir)
		plt.close('all')
		gc.collect()
		count+=1

automate(1)