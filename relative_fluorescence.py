#comparative intensity analysis of fluorescence images
#input a list of filepaths for images to be compared
#outputs a single image comparing images according to 
#a scale from 0 to 255 with an associated heat scale

from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.image as mpi
import numpy as np
import matplotlib.cm as cm

fig, axs = plt.subplots(6,1, figsize=(10.8,19.2))

output = '' #input a filepath and filename for a file without extension
image_list = [] #input a list of filepaths for the images for comparison
images = sorted(image_list) #keeps the images in the same order between runs

arrays = list()
for i, file in enumerate(images):
    print(file) #provides order of images as read by program
    image = mpi.imread(file)
    arrays.append(axs[i].imshow(image))

[ax.set_axis_off() for ax in axs.ravel()]

vmin = min(image.get_array().min() for image in arrays)
vmax = max(image.get_array().max() for image in arrays)
norm = colors.Normalize(vmin=vmin, vmax=vmax)

for img in arrays:
    img.set_norm(norm)
    img.set_cmap('magma') #choose color for heatmap ie. magma or viridis

fig.colorbar(arrays[0], ax=axs,  orientation='vertical', fraction=0.85)

plt.subplots_adjust(wspace= 5, hspace = 0.01)
fig.savefig(f'{output}.svg',format='svg',dpi=300) #saves image as vectorized image


