import cv2
import requests
import time

# Indirizzo del server Flask
SERVER_URL = "http://127.0.0.1:5000/process_image"

def capture_and_send_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Errore nell'aprire la webcam")
        return

    time_interval = 5  # Secondi tra un frame e l'altro
    last_capture_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Errore nel leggere il frame dalla webcam")
            break

        current_time = time.time()
        if current_time - last_capture_time >= time_interval:
            last_capture_time = current_time

            # Codifica il frame come immagine JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)

            # Invia il frame al server Flask
            response = requests.post(SERVER_URL, files={"image": img_encoded.tobytes()})
            print(response.json())

        # Mostra il video in tempo reale
        cv2.imshow('Client Webcam', frame)

        # Premi 'q' per uscire
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send_image()
