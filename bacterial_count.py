# segmentation algorithm to count bacteria
# in fungi using fluorescence based on 
# bacterial 16S rRNA gene and fungal 18S
# rRNA gene. 

import cv2
import numpy as np
from math import sqrt
from skimage.feature import blob_dog
import matplotlib.pyplot as plt

kernel = np.ones((3,3),np.uint8)
fungal_fp = ''    #filepath for fungal 18S image
bacterial_fp = '' #filepath for bacterial 16S image

def main():
    fungal_image = fungal_fp
    bacterial_image = bacterial_fp
    masked = createMask(fungal_image, bacterial_image)
    detectBlobs(masked)

# generates a mask outlining fungal hyphae
# generates new image that removes bacteria
# outside the fungal hyphae
def createMask(filename_a, filename_b):
    fungus = cv2.imread(filename_a)
    bacteria = cv2.imread(filename_b)
    bacteria_bw = bacteria[:,:,0]
    fungus_bw = fungus[:,:,0]
    ret, thresh = cv2.threshold(fungus_bw, 15, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_and(bacteria_bw, thresh)
    return mask

# runs spot detecting algorithm using ScikitImage
# based on a difference of Gaussian filter
# prints the number of bacteria per image
# generates an image of bacteria detected
# due to the change in scale bar from source images
# values should be calculated to determine object 
# per area of desired scale. 
def detectBlobs(image):
    spots = blob_dog(
        image=image,
        max_sigma=21,
        threshold=0.2
    )
    print(spots)
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.imshow(image)
    for blob in spots:
        y, x, r = blob
        c = plt.Circle(
            (x,y), 
            r, 
            color='white', 
            linewidth=1,
            fill=False
        )
        ax.add_patch(c)
    plt.show()   


if __name__ == '__main__':
    main()