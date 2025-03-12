import torch
import cv2
import os
from flask import Flask, render_template, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
import pathlib

# Workaround for Path issues on Windows
pathlib.PosixPath = pathlib.WindowsPath

# Create the Flask app
app = Flask(__name__)

# Load the custom YOLOv5 model
model_path = r'C:\Users\DELL\OneDrive\Desktop\camera\content\yolov5\best.pt'

try:
    # Load the YOLOv5 model with the custom trained weights
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False)
    model.eval()  # Set model to evaluation mode
    print("Custom model loaded successfully!")
except Exception as e:
    print(f"Error loading the model: {e}")

# Define the bin categories and colors
BIN_CATEGORIES = {
    'Plastic': {'color': 'Red', 'objects': ['Plastic', 'Plastic bag', 'bottle', 'plastic containers']},
    'Cans and Tetrapacks': {'color': 'Yellow', 'objects': ['cans', 'tetrapacks']},
    'Paper and Cardboard': {'color': 'Blue', 'objects': ['Paper', 'book', 'cardboard']},
    'Glass': {'color': 'Green', 'objects': ['glass', 'glass bottles', 'glass cups', 'mirror']},
    'E-waste': {'color': 'Black', 'objects': ['cell phone', 'laptop', 'charger', 'wires', 'earbuds', 'earphones', 'computer']},
    'Human': {'color': 'not racist', 'objects': ['person', 'human']}
}

def get_bin_info(object_name):
    for category, info in BIN_CATEGORIES.items():
        if object_name in info['objects']:
            return category, info['color']
    return 'Unknown', 'Unknown'

# Initialize the video capture (0 for default webcam)
camera = cv2.VideoCapture(0)

# Define upload folder for images
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Read the uploaded image
            img = cv2.imread(filepath)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Perform inference using the custom YOLOv5 model
            results = model(img_rgb)
            
            # Render the results (bounding boxes, labels) on the frame
            output_img = results.render()[0]
            output_filename = 'detected_' + filename
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            cv2.imwrite(output_filepath, output_img)

            # Process the results and prepare the output for the template
            detections = results.pandas().xyxy[0]
            results_list = []
            for _, row in detections.iterrows():
                object_name = row['name']
                bin_category, bin_color = get_bin_info(object_name)
                
                results_list.append({
                    'bin_category': f"{bin_category} ({bin_color})",
                    'location': (row['xmin'], row['ymin'])
                })

            return render_template('result.html', results=results_list, image_url='/static/uploads/' + output_filename)

        except Exception as e:
            return f"Error processing image with YOLOv5: {e}"
    else:
        return 'Invalid file type'

@app.route('/capture', methods=['GET'])
def capture():
    return redirect(url_for('video_feed'))

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            # Read frame from the camera
            success, frame = camera.read()
            if not success:
                break

            # Convert the frame from BGR (OpenCV format) to RGB (YOLOv5 expects RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Perform inference using the YOLOv5 model
            results = model(frame_rgb)  # Pass the RGB frame to the custom model
            
            # Render the results (bounding boxes, labels) on the frame
            results.render()  # Renders results on the frame

            # Convert the frame back to BGR for OpenCV display (since OpenCV expects BGR)
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            
            # Convert the frame to JPEG for streaming
            ret, jpeg = cv2.imencode('.jpg', frame_bgr)
            if ret:
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Return the response to stream the video feed with detection
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera', methods=['GET'])
def start_camera():
    if not camera.isOpened():
        camera.open(0)
    return redirect(url_for('video_feed'))

@app.route('/stop_camera', methods=['GET'])
def stop_camera():
    if camera.isOpened():
        camera.release()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

