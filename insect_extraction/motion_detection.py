import argparse
import os
import subprocess
import time
import warnings
import datetime
import imutils
from imutils.video import VideoStream
import json
import matplotlib.pyplot as plt
import pandas as pd
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
                help="path to the JSON configuration file")
ap.add_argument("-u", "--url", required=False,
                help="URL of Youtube stream")
ap.add_argument("-l", "--load", required=False,
                help="path to load existing observation file")
ap.add_argument("-w", "--write", required=False,
                help="path to save observation file")
args = vars(ap.parse_args())

# Filter warnings and load the configuration file
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# Initialize the camera and grab a reference to the video stream
if args["url"]:
    stream = subprocess.check_output(['youtube-dl', '-g', args["url"]]).strip()
    stream = stream.decode('utf-8')
else:
    stream = 0

# Start the video
cap = VideoStream(stream).start()

"""
Iinitialize the average frame, frame and motion counter and initialize
a time series to track motion frequency over time
"""
avg = None
motion_counter = 0
text = ""
load_path = args["load"]

if load_path:
    print("[INFO] Loading existing observation file...")
    time_series = pd.read_csv(load_path)
else:
    print("[INFO] No existing observations loaded. Gathering new observations...")
    time_series = pd.Series()

while True:
    # Capture frames from the video stream
    frame = cap.read()
    if frame is None:
        cap.stop()
        cap = VideoStream(stream).start()
        continue

    timestamp = datetime.datetime.now()

    # Resize the frame, convert it to grayscale and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If the average frame is None, initialize it
    if avg is None:
        print("[INFO] Starting background model...")
        avg = gray.copy().astype("float")
        continue

    """
    Accumulate the weighted average between the current frame and
    previous frames, then compute the difference between the current
    frame and the running average
    """
    cv2.accumulateWeighted(gray, avg, 0.5)
    frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    """
    Threshold the delta image, dilate the threshold image to fill
    in holes, then find contours on threshold image
    """
    thresh = cv2.threshold(frame_delta, conf["delta_thresh"], 255,
                           cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # Loop over the contours
    num_mtn_cnts = 0
    for c in cnts:
        # If the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"] or cv2.contourArea(c) > conf["max_area"]:
            continue

        # Compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        scale_factor = w / h

        # If the contour isn't rectangular, it isn't a bee being detected
        if scale_factor < 0.45:
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        num_mtn_cnts += 1
        text = "Motion Count: "

    # Check if motion was detected
    if text == "Motion Count: ":
        observation = pd.Series([num_mtn_cnts], index=[datetime.datetime.now()])
        time_series = time_series.append(observation)
        motion_counter += 1
        text += str(motion_counter)

    # Draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, text, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # Check to see if the frames should be displayed to screen
    if conf["show_video"]:
        # Display the feed
        cv2.imshow("Video Stream", frame)
        cv2.imshow("Frame Delta", frame_delta)
        key = cv2.waitKey(1) & 0xFF

        # IF the `q` key is pressed, break from the loop
        if key == ord("q"):
            break

cap.stop()
cv2.destroyAllWindows()

print("[INFO] The stream has ended!")
time_series = time_series.resample("15min").sum()
plt.style.use("ggplot")
time_series.plot(x='Time', y="Motion Frequency")
plt.show()

write_path = args["write"]
if write_path:
    write_path = os.path.join(write_path + "motion_observations.csv")
    print("[INFO] Writing observations to file:", write_path)
    time_series.to_csv(write_path)
