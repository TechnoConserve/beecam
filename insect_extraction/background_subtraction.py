import time

from imutils.video import FPS, FileVideoStream
import numpy as np
import cv2 as cv

cap = FileVideoStream('test30fps.h264').start()
time.sleep(1.0)
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

while cap.more():
    frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv.imshow('Original Frame', frame)
    cv.imshow('Masked Frame', fgmask)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cv.destroyAllWindows()
