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
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
