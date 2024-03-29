# Real-Time Camera Streaming, Face Detection, and Video Recording with Flask

This project demonstrates real-time camera streaming, face detection, and video recording using Flask. It utilizes OpenCV to capture video frames from the camera, detect faces, and record videos when faces are detected. Flask is used to serve the video stream over a web interface.

## Prerequisites

- Python 3.x
- OpenCV
- Flask

## Installation

1. Clone this repository:
git clone https://github.com/Astroisback/Security-Camera/


2. Install the required dependencies:
pip install opencv-python Flask

## Usage

1. Run the main file.

2. Open a web browser and navigate to `http://localhost:5000/` to view the live camera stream.

3. Press 'q' on your keyboard to stop the program and close the streaming window.

## Features

- Real-time camera streaming over a web interface.
- Date, time, and seconds displayed on the video stream.
- Face detection with bounding boxes around detected faces.
- Automatic screenshot capture of detected faces, saved in the "detected_faces" folder.
- Video recording when faces are detected, with recordings saved in the "recordings" folder.
- Adjustable frame rate for streaming and recording.
- Recording duration can be set (default is 10 seconds after the last face detection).

## Folder Structure

- `detected_faces`: Contains screenshots of detected faces.
- `recordings`: Contains recorded video files when faces are detected.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
