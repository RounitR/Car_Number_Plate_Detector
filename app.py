from flask import Flask, request, render_template, jsonify, url_for, send_file
import cv2
import numpy as np
import imutils
import easyocr
from collections import Counter
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'static'  # Store processed video in the static folder
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the video file
        most_common_plate, processed_video_path, detected_frame_path = process_video(filepath)
        
        # Remove uploaded file after processing
        os.remove(filepath)
        
        # Render result with detected frame and download button
        return render_template('upload.html', result=most_common_plate, result_video=processed_video_path, detected_frame=detected_frame_path)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error: Could not open video.", None, None

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    reader = easyocr.Reader(['en'])
    plate_pattern = re.compile(r'^[A-Z0-9]{7}$')
    valid_plates = []
    detected_frame = None
    
    # Output processed video
    output_video_path = os.path.join(app.config['PROCESSED_FOLDER'], 'output_with_plates.mp4')
    output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(bfilter, 30, 200)
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        locations = []

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                locations.append(approx)

        if locations:
            for location in locations:
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [location], 0, 255, -1)
                new_image = cv2.bitwise_and(frame, frame, mask=mask)

                (x, y) = np.where(mask == 255)
                (x1, y1) = np.min(x), np.min(y)
                (x2, y2) = np.max(x), np.max(y)
                cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

                result = reader.readtext(cropped_image)
                if result:
                    text = result[0][-2].replace(" ", "")
                    if plate_pattern.match(text):
                        valid_plates.append(text)
                        # Save the detected frame where a valid plate was found
                        if detected_frame is None:
                            detected_frame = frame.copy()
                            cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], 'detected_frame.jpg'), detected_frame)

                # Draw rectangle and add text to frame
                cv2.rectangle(frame, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)
                if result and plate_pattern.match(text):
                    cv2.putText(frame, text, (location[0][0][0], location[1][0][1] + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        output_video.write(frame)

    cap.release()
    output_video.release()

    if valid_plates:
        most_common_plate = Counter(valid_plates).most_common(1)[0][0]
        return most_common_plate, 'output_with_plates.mp4', 'detected_frame.jpg'
    else:
        return "No valid plates detected.", 'output_with_plates.mp4', 'detected_frame.jpg'

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)