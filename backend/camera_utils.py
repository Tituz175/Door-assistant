# camera_utils.py
import cv2


def initialize_camera():
    """Initialize the camera and set the frame dimensions."""
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1040)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 980)
    return cap


def deinitialize_camera(cap):
    """Release the camera when done."""
    cap.release()


if __name__ == "__main__":
    pass
