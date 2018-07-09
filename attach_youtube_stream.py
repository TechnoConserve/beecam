import argparse
import cv2
import pafy

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,
                help="URL of Youtube stream")
args = vars(ap.parse_args())

v_pafy = pafy.new(args["url"])
play = v_pafy.getbest()

# Start the video
cap = cv2.VideoCapture(play.url)
while True:
    ret, frame = cap.read()

    cv2.imshow('Frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
