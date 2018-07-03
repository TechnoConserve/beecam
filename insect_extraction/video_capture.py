from imutils.video import FPS, FileVideoStream
import numpy as np
import cv2
import time

stream = FileVideoStream('test30fps.h264').start()
time.sleep(1.0)
fps = FPS().start()

while stream.more():
    # Capture frame-by-frame
    frame = stream.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    fps.update()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# When everything done, release the capture
cv2.destroyAllWindows()
stream.stop()
