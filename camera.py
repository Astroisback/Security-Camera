import cv2
import datetime
import threading
import os

# Global variables for video capture
video_capture = None
frame_size = None
video_thread = None
video_thread_lock = threading.Lock()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")


def start_video_capture(width, height):
    global video_capture, frame_size , current_datetime , fourcc
    if video_capture is not None:
        video_capture.release()  # Release the existing capture

    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    video_capture.set(cv2.CAP_PROP_FPS, 28)  # Set the frame rate to 28 fps
    frame_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))



        
def generate_frames(user_data):
    global video_capture, frame_size

    is_recording = False
    recording_start_time = None
    SECONDS_TO_RECORD = 10

    if video_capture is None:
        print("Error: Video capture not initialized.")
        return

    video_writer = None # Declare video_writer outside the while loop
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Face and Body Detection
        faces = face_cascade.detectMultiScale(grayscale_frame, 1.3, 5)
        bodies = body_cascade.detectMultiScale(grayscale_frame, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recording Logic (Corrected)
        if (len(faces) > 0 or len(bodies) > 0) and user_data is not None:  
            if not is_recording:
                is_recording = True
                recording_start_time = datetime.datetime.now()

                # Ensure the directory exists, create it if not
                os.makedirs(user_data, exist_ok=True)

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video_writer = cv2.VideoWriter(f"{user_data}/recording_{current_datetime}.mp4", fourcc, 28.0, frame_size)
                print("Started Recording!")
 
        # Stop Recording Logic (Improved)
        if is_recording:
            # If video_writer was created, write the frame
            if video_writer is not None:
                video_writer.write(frame)

            # Stop recording after the specified duration or if face/body not detected
            if ((datetime.datetime.now() - recording_start_time).total_seconds() >= SECONDS_TO_RECORD
                or not (faces or bodies)):  

                is_recording = False
                if video_writer is not None:  # Release the writer if recording has stopped
                    video_writer.release()
                    video_writer = None
                    print("Video Recording Stopped")

        # Display timestamp on the frame
        cv2.putText(frame, current_datetime, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


