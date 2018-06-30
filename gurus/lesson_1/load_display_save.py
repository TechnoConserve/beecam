import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-o", "--output", required=True, help="Path to save new image")
args = vars(ap.parse_args())

# Load the image and show some basic information on it
image = cv2.imread(args["image"])
print("Width: {} pixels".format(image.shape[1]))
print("Height: {} pixels".format(image.shape[0]))
print("Channels: ", image.shape[2])

# Show the image and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)

# Save the image -- OpenCV handles converting filetypes automatically
cv2.imwrite(args["output"], image)
