import cv2

# Load the image and show it
image = cv2.imread("../images/florida_trip.png")
cv2.imshow("Original", image)

# Cropping an image is accomplished using simple NumPy array slices
# Let's crop the face from the image
face = image[85:250, 85:220]
cv2.imshow("Face", face)
cv2.waitKey(0)

# And now lets crop the entire body
body = image[90:450, 0:290]
cv2.imshow("Body", body)
cv2.waitKey(0)

people = image[173:235, 13:81]
cv2.imshow("People", people)
cv2.waitKey(0)
