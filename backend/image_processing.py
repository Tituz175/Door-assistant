# image_processing.py
import cv2


def preprocess_frame(frame):
    """Convert the frame to grayscale and apply Gaussian blur."""
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
    return frame_bw


def detect_movement(frame_bw, start_frame, detection_counter):
    """Detect movement in the frame by comparing it to a reference frame."""
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    start_frame = frame_bw

    if threshold.sum() > 10000000:
        detection_counter += 1
    else:
        if detection_counter > 0:
            detection_counter -= 1

    return threshold, start_frame, detection_counter


if __name__ == "__main__":
    pass
