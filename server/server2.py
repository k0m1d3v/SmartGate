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
listaTarghe = []  # Lista per le targhe

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
    npimg = np.frombuffer(file.read(), np.uint8)  # Usa frombuffer per evitare avvisi deprecati
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

    # Prepara la risposta da inviare al client
    return jsonify({"Persona rilevata": face_names, "Targa rilevata": plate_text})


# Funzione per il riconoscimento targhe con Google Vision
def detect_license_plate_text(image):
    success, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return None

    # Definire i limiti del riquadro per le targhe
    min_x = 100  # X minimo del riquadro
    max_x = 500  # X massimo del riquadro
    min_y = 200  # Y minimo del riquadro
    max_y = 400  # Y massimo del riquadro

    for text in texts:
        # Ottieni i vertici del riquadro attorno al testo
        vertices = text.bounding_poly.vertices
        x_coords = [vertex.x for vertex in vertices]
        y_coords = [vertex.y for vertex in vertices]

        # Controlla se il testo rilevato è all'interno del riquadro definito
        if (min_x <= min(x_coords) <= max_x) and (min_y <= min(y_coords) <= max_y):
            raw_text = text.description.strip()
            filtered_text = filter_alphanumeric(raw_text)

            # Filtro per lunghezza e formato della targa
            if is_valid_license_plate(filtered_text):
                return filtered_text

    return None


# Funzione per verificare se il testo è una targa valida
def is_valid_license_plate(text):
    # Esempio: Controlla se la targa ha un formato specifico (es. 2 lettere, 3 numeri, 2 lettere)
    pattern = r'^[A-Z]{2}\d{3}[A-Z]{2}$'  # Modifica il pattern in base al formato delle tue targhe
    return bool(re.match(pattern, text))


# Nuovo endpoint per caricare volti
@app.route('/upload_face', methods=['POST'])
def upload_face():
    file = request.files['image']
    filename = file.filename
    # Salva l'immagine nella directory known_faces
    file.save(os.path.join(KNOWN_FACES_DIR, filename))

    # Ricarica i volti conosciuti dopo aver aggiunto la nuova immagine
    load_known_faces(KNOWN_FACES_DIR)
    return jsonify({"message": "Face uploaded successfully", "name": os.path.splitext(filename)[0]})


# Nuovo endpoint per aggiungere targhe
@app.route('/add_plate', methods=['POST'])
def add_plate():
    plate = request.json.get('plate')
    if plate and is_valid_license_plate(plate):
        listaTarghe.append(plate)
        return jsonify({"message": "Plate added successfully", "plate": plate})
    else:
        return jsonify({"error": "Invalid plate format"}), 400


# Avvia il server Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
