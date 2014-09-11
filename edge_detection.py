from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np

im = np.zeros((256, 256))
for (i,x) in enumerate(im):
	if(i == 128):
		for i2 in range(len(x)):
			x[i2] = 1
# im[64:-64, 64:-64] = 1
# plt.figure(figsize=(5, 5))
# plt.imshow(im)

# im = ndimage.rotate(im, 15, mode='constant')
# im = ndimage.gaussian_filter(im, 8)

sx = ndimage.sobel(im, axis=0, mode='constant')
sy = ndimage.sobel(im, axis=1, mode='constant')
sob = np.hypot(sx, sy)

plt.figure(figsize=(5, 5))
plt.imshow(sob)
plt.axis('off')
plt.title('Sobel filter', fontsize=20)

plt.show()