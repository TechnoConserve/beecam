import cv2

# Load our image and convert it to grayscale
image = cv2.imread("faces_image.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the face detector and detect faces in the image
detector = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=9,
                                  minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

# Loop over the faces and draw a rectangle surrounding each
for (x, y, w, h) in rects:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the detected faces
cv2.imshow("Faces", image)
cv2.waitKey(0)
