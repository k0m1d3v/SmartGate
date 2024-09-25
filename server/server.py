import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
import face_recognition
from google.cloud import vision
from google.cloud.vision_v1 import types
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le route

KNOWN_FACES_DIR = "known_faces"
PLATES_FILE = "targhe.txt"

known_faces = []
known_names = []


# Carica e codifica i volti conosciuti
def load_known_faces(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_faces.append(encoding[0])
                known_names.append(os.path.splitext(filename)[0])


load_known_faces(KNOWN_FACES_DIR)
print(f"Volti conosciuti caricati: {known_names}")


# Funzione per caricare le targhe da un file
def load_known_plates(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []


# Funzione per aggiungere una targa al file
def add_plate_to_file(plate, file_path):
    with open(file_path, "a") as file:
        file.write(f"{plate}\n")


known_plates = load_known_plates(PLATES_FILE)


# Funzione per filtrare solo caratteri alfanumerici
def filter_alphanumeric(text):
    return re.sub(r'[^A-Za-z0-9]', '', text)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'platetextrecognition-7684c9cf2659.json'
client = vision.ImageAnnotatorClient()


@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_rgb)
    face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
        else:
            name = "Sconosciuto"
        face_names.append(name)

    plate_text = detect_license_plate_text(img)

    return jsonify({"Persona rilevata": face_names, "Targa rilevata": plate_text})


@app.route('/upload_face', methods=['POST'])
def upload_face():
    file = request.files['image']
    if file:
        filename = file.filename
        filepath = os.path.join(KNOWN_FACES_DIR, filename)
        file.save(filepath)

        load_known_faces(KNOWN_FACES_DIR)
        return jsonify({"message": "Face uploaded and processed."})
    else:
        return jsonify({"error": "No file uploaded."}), 400


@app.route('/add_plate', methods=['POST'])
def add_plate():
    data = request.get_json()
    plate = data.get('plate')

    if plate and is_valid_license_plate(plate):
        known_plates.append(plate)
        add_plate_to_file(plate, PLATES_FILE)
        return jsonify({"message": "Plate added successfully."})
    else:
        return jsonify({"error": "Invalid plate format."}), 400


def detect_license_plate_text(image):
    success, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return None

    min_x = 100
    max_x = 500
    min_y = 200
    max_y = 400

    for text in texts:
        vertices = text.bounding_poly.vertices
        x_coords = [vertex.x for vertex in vertices]
        y_coords = [vertex.y for vertex in vertices]

        if (min_x <= min(x_coords) <= max_x) and (min_y <= min(y_coords) <= max_y):
            raw_text = text.description.strip()
            filtered_text = filter_alphanumeric(raw_text)

            if is_valid_license_plate(filtered_text):
                return filtered_text

    return None


def is_valid_license_plate(text):
    pattern = r'^[A-Z]{2}\d{3}[A-Z]{2}$'
    return bool(re.match(pattern, text))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
