from datetime import datetime

from imutils import contours
from imutils.video import VideoStream
import argparse
import imutils
import numpy as np
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--reference", required=True,
                help="path to reference OCR font image")
ap.add_argument("-t", "--tracker", type=str, default="csrt",
                help="OpenCV object tracker type")
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
args = vars(ap.parse_args())


def get_contours(thresh, threshold_area=2000):
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = contours.sort_contours(cnts, method="left-to-right")[0]

    final_contours = []
    # Filter contours
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > threshold_area:
            final_contours.append(cnt)

    return final_contours


def get_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return final


def define_reference_digits(ref_cnts):
    digits = {}
    # Loop over the OCR reference contours
    for (i, c) in enumerate(ref_cnts):
        # compute the bounding box for the digit, extract it, and resize
        # it to a fixed size
        (x, y, w, h) = cv2.boundingRect(c)
        roi = ref[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))

        # update the digits dictionary, mapping the digit name to the ROI
        digits[i] = roi

    return digits


def classify_digits(img, reference_digits):
    img = imutils.resize(img, height=150)
    img_thresh = get_thresh(img)
    img_cnts = get_contours(img_thresh)

    output = []
    for c in img_cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))

        # Initialize a list of template matching scores
        scores = []

        # Loop over the reference digit name and digit ROI
        for (digit, digitROI) in reference_digits.items():
            # Apply correlation-based template matching, take the
            # score, and update the scores list
            result = cv2.matchTemplate(roi, digitROI,
                                       cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)

        # The classification for the digit ROI will be the reference
        # digit name with the largest template matching score
        max_score = str(np.argmax(scores))
        output.append((max_score, roi))

    return output


# Initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerMIL_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# Initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()


def main(reference_digits):
    vs = get_video_stream()
    time_parsable = False

    # Loop over frames from the video stream
    while True:
        # Grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame[1] if args.get("video", False) else frame

        # Check to see if we have reached the end of the stream
        if frame is None:
            break

        # Grab the updated bounding box coordinates (if any) for each
        # object that is being tracked
        (success, boxes) = trackers.update(frame)

        # Loop over the bounding boxes and draw them on the frame
        for box in boxes:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if reference_digits:
            while time_parsable is False:
                ts_box = get_timestamp_box()
                frame_time = get_frame_time(frame, reference_digits, ts_box)
                if frame_time is not None:
                    time_parsable = True

            frame_time = get_frame_time(frame, reference_digits, ts_box)

            cv2.rectangle(frame, (int(ts_box[0]), int(ts_box[1])),
                          (int(ts_box[0] + ts_box[2]), int(ts_box[1] + ts_box[3])), (0, 0, 255), 2)
            cv2.putText(frame, frame_time.strftime("%Y-%m-%d %H:%M:%S"), (int(ts_box[0]) - 30, int(ts_box[1]) + 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # Show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(0) & 0xFF

        # If the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # Select the bounding box of the object we want to track (make
            # sure to press ENTER or SPACE after selecting the ROI)
            box = cv2.selectROI("Object Tracker Selection", frame, fromCenter=False,
                                showCrosshair=True)

            if box == (0, 0, 0, 0):
                # Selection canceled
                continue

            # Create a new object tracker for the bounding box and add it
            # to our multi-object tracker
            tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
            trackers.add(tracker, frame, box)

        elif key == ord("q"):
            break

    # If we are using a webcam, release the pointer
    if not args.get("video", False):
        vs.stop()

    # Otherwise, release the file pointer
    else:
        vs.release()

    # Close all windows
    cv2.destroyAllWindows()


def get_frame_time(frame, reference_digits, ts_box):
    timestamp_area = frame[int(ts_box[1]):int(ts_box[1] + ts_box[3]), int(ts_box[0]):int(ts_box[0] + ts_box[2])]
    frame_time = process_timestamp_area(reference_digits, timestamp_area)
    return frame_time


def process_timestamp_area(reference_digits, timestamp_area):
    (h, w) = timestamp_area.shape[:2]

    first_line = timestamp_area[:int(h / 2), :w]
    fl_classification = classify_digits(first_line, reference_digits)
    fl_labels = [digit[0] for digit in fl_classification]

    second_line = timestamp_area[int(h / 2):, :w]
    sl_classification = classify_digits(second_line, reference_digits)
    sl_labels = [digit[0] for digit in sl_classification]

    labels = ''.join(fl_labels + sl_labels)
    try:
        timestamp = datetime.strptime(labels[:-2], "%Y%m%d%H%M%S")
    except ValueError:
        print("[!] Timestamp processing failed!\n")
        print("Please try to reselect the area where the timestamp information appears in the frame.")
        return None
    return timestamp


def get_timestamp_box():
    vs = get_video_stream()
    print("Select the area in the frame you would like characters to be recognized.")
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    ts_box = cv2.selectROI("Timestamp Area Selection", frame, fromCenter=False,
                           showCrosshair=True)
    return ts_box


def get_video_stream():
    # Grab a reference to the video file if passed as an argument
    if not args.get("video", False):
        print("[INFO] Starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)

    # Otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])

    return vs


if __name__ == "__main__":
    ref_digits = None

    # If given, parse the reference image for digit classification
    if args.get("reference", False):
        ref = cv2.imread(args.get("reference"))
        # Take a threshold of the image before finding contours
        thresh = get_thresh(ref)
        # Get contours of the reference image. Each should represent a digit
        # for matching against each frame in the video stream
        reference_contours = get_contours(thresh)
        # Get the reference digits
        ref_digits = define_reference_digits(reference_contours)

    main(ref_digits)
