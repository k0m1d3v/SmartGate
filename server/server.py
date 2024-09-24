import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
import face_recognition
from google.cloud import vision
from google.cloud.vision_v1 import types
import re

# Inizializza l'app Flask
app = Flask(__name__)

# Percorso alla cartella dei volti conosciuti
KNOWN_FACES_DIR = "known_faces"

# Carica e codifica i volti conosciuti
known_faces = []
known_names = []

def load_known_faces(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:  # Controlla che l'immagine abbia un volto
                known_faces.append(encoding[0])
                known_names.append(os.path.splitext(filename)[0])

load_known_faces(KNOWN_FACES_DIR)
print(f"Volti conosciuti caricati: {known_names}")

# Funzione per filtrare solo caratteri alfanumerici
def filter_alphanumeric(text):
    return re.sub(r'[^A-Za-z0-9]', '', text)

# Configurazione Google Vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'platetextrecognition-7684c9cf2659.json'
client = vision.ImageAnnotatorClient()

# Riconoscimento targhe e volti dal frame ricevuto dal client
@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    npimg = np.fromstring(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Converti l'immagine in RGB per face_recognition
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Rileva volti nell'immagine
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

    # Rilevamento targhe
    plate_text = detect_license_plate_text(img)

    return jsonify({"faces": face_names, "license_plate": plate_text})

# Funzione per il riconoscimento targhe con Google Vision
def detect_license_plate_text(image):
    success, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return None

    raw_text = texts[0].description.strip()
    filtered_text = filter_alphanumeric(raw_text)
    return filtered_text if filtered_text else None

# Avvia il server Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
