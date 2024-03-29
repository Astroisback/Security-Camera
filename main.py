import cv2
import datetime
from flask import Flask, Response
import os

app = Flask(__name__)


video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 28)  # Set the frame rate to 28 fps
frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")


if not os.path.exists("detected_faces"):
    os.makedirs("detected_faces")
if not os.path.exists("recordings"):
    os.makedirs("recordings")


def generate_frames():
    global video_capture
    is_recording = False
    video_writer = None
    recording_start_time = None
    SECONDS_TO_RECORD = 10  

    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
           
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            
            grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(grayscale_frame, 1.3, 5)
            bodies = body_cascade.detectMultiScale(grayscale_frame, 1.3, 5)

           
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
              
                face_image = frame[y:y+h, x:x+w]
                cv2.imwrite(f"detected_faces/face_{current_datetime}.jpg", face_image)

               
                if not is_recording:
                    is_recording = True
                    recording_start_time = datetime.datetime.now()
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    video_writer = cv2.VideoWriter(f"recordings/recording_{current_datetime}.mp4", fourcc, 28.0, frame_size)

            
            for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

           
            cv2.putText(frame, current_datetime, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Record video if a face was detected
            if is_recording:
                video_writer.write(frame)
                # Stop recording after the specified duration
                if (datetime.datetime.now() - recording_start_time).total_seconds() >= SECONDS_TO_RECORD:
                    is_recording = False
                    video_writer.release()

           
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
