import cv2
import time
import datetime
from flask import Flask, Response

app = Flask(__name__)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, 28)
frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))

def generate_frames():
    global video_capture
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, current_datetime, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

video_capture = cv2.VideoCapture(0)
is_detection_active = False
detection_stopped_time = None
is_timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 7
frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

while True:
    _, frame = video_capture.read()
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayscale_frame, 1.3, 5)
    bodies = body_cascade.detectMultiScale(grayscale_frame, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if is_detection_active:
            is_timer_started = False
        else:
            is_detection_active = True
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            video_writer = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 28.0, frame_size)
    elif is_detection_active:
        if is_timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                is_detection_active = False
                is_timer_started = False
                video_writer.release()
        else:
            is_timer_started = True
            detection_stopped_time = time.time()

    if is_detection_active:
        video_writer.write(frame)

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
