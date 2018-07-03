"""
A script to process a screenshot from a raspberry pi camera to make it easier
to identify bees in the image.

Follows tutorial from:
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
The original image looks down thru a screen mesh onto the tops of bee
hive frames over which bees will be crawling.
"""
img = cv2.imread('../pyimagesearch/images/bees.jpg', 0)
img = cv2.medianBlur(img, 5)

# Global thresholding seems to work best for preserving the images
ret, th1 = cv2.threshold(img, 110, 35, cv2.THRESH_BINARY)

"""
Both adaptive mean and adaptive gaussian thresholding see the mesh 
rather than the bees.
"""
th2 = cv2.adaptiveThreshold(img, 205, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 5, 11)
th3 = cv2.adaptiveThreshold(img, 205, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 5, 11)

titles = ['Original Image', 'Global Thresholding (v = 205)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()

"""
Binarization

Binarization is meant for bimodal images, which doesn't work
very well for our image since the pixel intensities exist
along a gradient. The corners are darker and more out of focus
compared to the center of the photo so this method ends up
not working very well.
"""
img = cv2.imread('../pyimagesearch/images/bees.jpg', 0)

# global thresholding
ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Otsu's thresholding
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(img, (5, 5), 0)
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# plot all the images and their histograms
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
          'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
          'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

for i in range(3):
    plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
    plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
    plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
    plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
plt.show()
