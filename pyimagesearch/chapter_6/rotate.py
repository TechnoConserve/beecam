import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)
cv2.waitKey(0)

(h, w) = image.shape[:2]
(cX, cY) = (w / 2, h / 2)

M = cv2.getRotationMatrix2D((cX, cY), 45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("Rotated by 45 Degrees", rotated)
cv2.waitKey(0)

M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("Rotated by -90 Degrees", rotated)
cv2.waitKey(0)

# Rotate our image around an arbitrary point rather than the center
M = cv2.getRotationMatrix2D((cX -50, cY - 50), 45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("Rotated by Offset & 45 Degrees", rotated)
cv2.waitKey(0)

"""
Finally, let's use our helper function in imutils to rotate by 180
degrees (flipping it upside down)
"""
rotated = imutils.rotate(image, 180)
cv2.imshow("Rotated by 180 Degrees", rotated)
cv2.waitKey(0)
