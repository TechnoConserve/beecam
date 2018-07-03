import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

"""
Images are NumPy arrays, stored as unsigned 8 bit integers. This implies
that the values of our pixels will be in the range [0, 255]; when using
functions like cv2.add and cv2.subtract, values will be clipped to this
range, even if the added or subtracted values fall outside the range of
[0, 255]. Check out this example
"""
print("Max of 255: {}".format(str(cv2.add(np.uint8([200]), np.uint8([100])))))
print("Min of 0: {}".format(str(cv2.subtract(np.uint8([50]), np.uint8([100])))))

"""
NOTE: If you use NumPy arithmetic operations on these arrays, the value
will be modulo (wrap around) instead of being clipped to the [0, 255]
range. This is important to keep in mind when working with images.
"""
print("Wrap around: {}".format(str(np.uint8([200]) + np.uint8([100]))))
print("Wrap around: {}".format(str(np.uint8([50]) - np.uint8([100]))))

"""
Let's increase the intensity of all pixels in our image by 100. We
accomplish this by constructing a NumPy array that is the same size
of our matrix (filled with ones) and then multiplying it by 100 to
create an array filled with 100's, then we simply add the images 
together; notice how the image is 'brighter'
"""
M = np.ones(image.shape, dtype="uint8") * 100
added = cv2.add(image, M)
cv2.imshow("Added", added)

# Similarly, we can subtract 50 from all pixels to make them darker
M = np.ones(image.shape, dtype="uint8") * 50
subtracted = cv2.subtract(image, M)
cv2.imshow("Subtracted", subtracted)
cv2.waitKey(0)
