from flask import Flask, render_template, request, Response , jsonify
from camera import *  
from utlis import *  
import time
import datetime
import os
user_data = None
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    system_info = get_system_info()
    return render_template('index.html', system_info=system_info)

@app.route('/set_resolution', methods=['POST'])
def set_resolution():
    resolution = request.form['resolution']
    try:
        width, height = map(int, resolution.split('x'))
        with video_thread_lock:
            
            start_video_capture(width, height)
    except ValueError:
        pass
    return render_template('index.html', system_info=get_system_info)


@app.route('/save_file', methods=['GET', 'POST'])
def test():
     global user_data

     if request.method == 'POST':
        name = request.form['name']

        user_data = name
        return f"System will now record and store the data as per the destination you selected, {name}." 
     return render_template('index.html',system_info=get_system_info)

@app.route('/video_feed')
def video_feed():
    global user_data
    return Response(generate_frames(user_data), mimetype='multipart/x-mixed-replace; boundary=frame') 



if __name__ == "__main__":
    start_video_capture(640, 480)  # Start video capture initially
    app.run(debug=True, host='0.0.0.0')

   
