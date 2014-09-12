from quasar_data import *
import wavelength_mapping
from init_plot import *

import gc
import matplotlib.pyplot as plt
import random
import csv

def start():
	max_radius = 1000
	plotsPerFigure = 20

	headers = (Header("1413/Image_D/s90/mapmeta.dat"),Header("1413/Image_A/s90/mapmeta.dat"))
	magFiles = ("1413/Image_D/s90/map.bin","1413/Image_A/s90/map.bin")
	quasar = q8

	basedir = "/home/josh/Dropbox/MagWavelengthPlots/H1413+117/"
	filename = "multiple_gaussians"
	saveDir = basedir+filename
	fig = plt.figure(figsize=(13,7))
	ax = fig.add_axes([0.06, 0.05, 0.6, 0.9])
	plots = plotsPerFigure*[None]
	for i in range(plotsPerFigure):
		print("generating plot",(i+1),"of",plotsPerFigure)
		centerx1 = random.randint(max_radius,headers[0].IMAGE_WIDTH-max_radius)
		centery1 = random.randint(max_radius,headers[0].IMAGE_HEIGHT-max_radius)
		centerx2 = random.randint(max_radius,headers[1].IMAGE_WIDTH-max_radius)
		centery2 = random.randint(max_radius,headers[1].IMAGE_HEIGHT-max_radius)
		diskDetails = DiskDetails(quasar.red_shift, quasar.wavelengths, quasar.einstein_radius,\
					(((centerx1,centery1),(centerx2,centery2)),max_radius),None)
		plots[i] = plotRadii(ax,None,headers, magFiles,diskDetails)
	plt.savefig(saveDir)
	plt.close('all')
	
	gc.collect()

start()
