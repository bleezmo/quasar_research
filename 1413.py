from quasar_data import *
import wavelength_mapping
from init_plot import *

import gc
import matplotlib.pyplot as plt
import random

def automate(countMax):
	#initialization stuff
	max_radius = 600
	headers = (Header("1413/Image_A/s90/mapmeta.dat"),Header("1413/Image_D/s90/mapmeta.dat"))
	magFiles = ("1413/Image_A/s90/map.bin","1413/Image_D/s90/map.bin")
	quasar = 
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
		centerx1 = random.randint(max_radius,headers[0].IMAGE_WIDTH-max_radius)
		centery1 = random.randint(max_radius,headers[0].IMAGE_HEIGHT-max_radius)
		centerx2 = random.randint(max_radius,headers[1].IMAGE_WIDTH-max_radius)
		centery2 = random.randint(max_radius,headers[1].IMAGE_HEIGHT-max_radius)
		filename = "center1:"+str(centerx1)+","+str(centery1)+"&"\
						+"center2:"+str(centerx2)+","+str(centery2)+"WithBuildupAndPlanck"
		saveDir = basedir+filename
		print(filename)
		fig = plt.figure(figsize=(13,7))
		ax = fig.add_axes([0.06, 0.05, 0.6, 0.9])
		for i,annulus_removed in enumerate(annuli_removed):
			print("generating map",i+1,"of",len(annuli_removed))
			diskDetails = DiskDetails(quasar.red_shift, quasar.wavelengths, quasar.einstein_radius,\
						(((centerx1,centery1),(centerx2,centery2)),max_radius),\
						annulus_removed)
			plot(ax,maplegend[i],headers, magFiles,diskDetails)
		plt.savefig(saveDir)
		plt.close('all')
		gc.collect()
		count+=1

automate(1)