import imp
import map_objects
from quasar_data import *
import wavelength_mapping

import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors

def reloadModules():
	imp.reload(map_objects)
	imp.reload(wavelength_mapping)

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

def loadDisk(header, magMapFile,wavelengths,einsteinRadius,diskCenter,diskSize,annulus_removed):
	print("loading magnification map and header file")
	file = open(magMapFile,"rb")
	pixel_size = (header.quasar_size * einsteinRadius)/header.IMAGE_WIDTH
	mag_array = np.fromfile(file,np.dtype("i4")).reshape(header.IMAGE_WIDTH,header.IMAGE_HEIGHT)
	file.close()
	disk = map_objects.Disk(diskCenter,diskSize,pixel_size)
	print("computing wavelengths in disk")
	stepsize = diskSize//300 #increase step size to compute disk in reasonable amount time
	disk.computeWavelengths(wavelength_mapping.PlanckRadiusMapping,\
		wavelengths,smooth_step = stepsize if stepsize > 0 else 1,annulus_removed=annulus_removed)
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