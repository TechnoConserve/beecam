"""
Testing based on
https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
"""
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
raw_capture = PiRGBArray(camera)

# Allow the camera to warm up
time.sleep(0.1)

# Grab an image from the camera
camera.capture(raw_capture, format="bgr")
image = raw_capture.array

# Display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)