import numpy as np
import cv2 as cv

cap = cv.VideoCapture('test30fps.h264')
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv.imshow('Original Frame', frame)
    cv.imshow('Masked Frame', fgmask)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
