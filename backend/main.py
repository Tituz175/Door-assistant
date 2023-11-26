import os
import cv2
import mediapipe as mp
from camera_utils import initialize_camera, deinitialize_camera
from image_processing import preprocess_frame, detect_movement
from image_classifier import image_classifier
from notification_utils import send_notification


class VideoProcessor:
    def __init__(self):
        # Initialize variables and Mediapipe components
        self.cap = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
            max_num_faces=2, refine_landmarks=True)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.face_seen = False
        self.detection_counter = 0
        self.start_frame = None

    def camera_start(self):
        # Start the camera and capture the initial frame
        self.cap = initialize_camera()
        _, self.start_frame = self.cap.read()
        self.start_frame = preprocess_frame(self.start_frame)

    def camera_stop(self):
        # Stop the camera
        deinitialize_camera(self.cap)

    def main(self):
        while self.cap.isOpened():
            # Capture a frame from the camera
            _, frame = self.cap.read()
            frame_bw = preprocess_frame(frame)

            # Detect movement in the frame
            threshold, self.start_frame, self.detection_counter = detect_movement(
                frame_bw, self.start_frame, self.detection_counter)

            if self.detection_counter > 15:
                # Draw a rectangle around the detected movement
                x, y, w, h = cv2.boundingRect(threshold)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Process the frame with face detection
                imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.faceMesh.process(imageRGB)

                if results.multi_face_landmarks:
                    # Draw face landmarks if detected
                    for faceLMs in results.multi_face_landmarks:
                        self.mpDraw.draw_landmarks(
                            frame, faceLMs, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
                    self.face_seen = True
            else:
                # Process the frame with face detection
                imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.faceMesh.process(imageRGB)

                if results.multi_face_landmarks:
                    # Draw face landmarks if detected
                    for faceLMs in results.multi_face_landmarks:
                        self.mpDraw.draw_landmarks(
                            frame, faceLMs, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)

                    # Perform image classification if no image is saved, and a face has been previously seen
                    if not (os.path.exists("backend/captured_image.jpg")) and self.face_seen:
                        cv2.imwrite("backend/captured_image.jpg", frame)
                        captured_image = cv2.imread(
                            "backend/captured_image.jpg")
                        obj = image_classifier(captured_image, r"C:\Users\tobit\Documents\nmhu\ssd\fall '23\BSSD 6000\image rec\full-project\backend\keras_model.h5",
                                               r"C:\Users\tobit\Documents\nmhu\ssd\fall '23\BSSD 6000\image rec\full-project\backend\labels.txt")

                        # Send notification if the image classification is "human"
                        if obj.strip() == "human":
                            send_notification()
                            os.remove("backend/captured_image.jpg")
                            self.face_seen = False

            # Display the frame with overlays
            cv2.imshow("Cam", frame)

            # Check for key press to exit the loop
            key_pressed = cv2.waitKey(30)
            if key_pressed == ord("q"):
                break

        # Stop the camera when the loop exits
        self.camera_stop()


# Entry point for the script
if __name__ == "__main__":
    # Create an instance of the VideoProcessor class
    video_processor = VideoProcessor()

    # Start the camera and run the main loop
    video_processor.camera_start()
    video_processor.main()
