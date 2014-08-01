class QuasarDetails:
	def __init__(self,red_shift,wavelengths,einstein_radius = -1):
		self.red_shift = red_shift
		self.wavelengths = wavelengths
		self.einstein_radius = einstein_radius

# MGJ0414+0534 (rs=2.64)wavelengths(nm):
# WFC3/UVIS Imaging F467M - 468.3
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
q1=QuasarDetails(2.64,(468.3,621.9,761.2,843.6,1248.6))

#RXJ0911+0551 (rs=2.80)wavelengths(nm):
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F689M - 687.6
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q2=QuasarDetails(2.8,(544.7,621.9,687.6,843.6,1248.6,1536.9))

#SDSSJ0924+0219 (rs=1.524) wavelengths(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F105W - 1055.2
# WFC3/IR Imaging F160W - 1536.9
# Einstein radius - 4.372277 x 10^14 m
q3=QuasarDetails(1.524,(410.9,544.7,621.9,843.6,1055.2,1536.9), 437227700000000)

# PG1115+080 (rs=1.72) wavelengths(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
# WFC3/IR Imaging F105W - 1055.2
q4=QuasarDetails(1.72,(410.9,621.9,843.6,1248.6,1536.9,1055.2))

# B1422+231 (rs=3.62) wavelengths(nm):
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
# WFC3/IR Imaging F105W - 1055.2
q5=QuasarDetails(3.62,(621.9,761.2,843.6,1248.6,1536.9,1055.2))

# WFIJ2026-4536 (rs=2.23)wavelength(nm):
# WFC3/UVIS Imaging F410M - 410.9
# WFC3/UVIS Imaging F547M - 544.7
# WFC3/UVIS Imaging F689M - 687.6
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F845M - 843.6
# WFC3/IR Imaging F105W - 1055.2
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q6=QuasarDetails(2.23,(410.9,544.7,687.6,761.2,843.6,1055.2,1248.6,1536.9))

# WFIJ2033-4723 (rs=1.66) wavelengths(nm):
# WFC3/UVIS Imaging F467M - 468.3
# WFC3/UVIS Imaging F621M - 621.9
# WFC3/UVIS Imaging F763M - 761.2
# WFC3/UVIS Imaging F814W - 802.4
# WFC3/IR Imaging F125W - 1248.6
# WFC3/IR Imaging F160W - 1536.9
q7=QuasarDetails(1.66,(468.3,621.9,761.2,802.4,1248.6,1536.9))