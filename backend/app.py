from flask import Flask, jsonify, request
from flask_cors import CORS
from main import VideoProcessor  # Assuming VideoProcessor is defined in main module

# Create a Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Create an instance of the VideoProcessor class
video_processor = VideoProcessor()


# Route to start the camera
@app.route('/start_camera')
def start_camera():
    # Start the camera and perform any other necessary actions
    video_processor.camera_start()
    video_processor.main()  # Assuming this method contains the main logic
    return jsonify(message="Camera started."), 200


# Route to stop the camera
@app.route('/stop_camera')
def stop_camera():
    # Stop the camera
    video_processor.camera_stop()
    return jsonify(message="Camera stopped."), 200


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
