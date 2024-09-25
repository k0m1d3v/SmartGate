import cv2
import requests
import time

# Indirizzo del server Flask
SERVER_URL = "http://<your-servr-ip>:5000/process_image"


def capture_and_send_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Errore nell'aprire la webcam")
        return

    time_interval = 4  # Secondi tra un frame e l'altro
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

            try:
                # Invia il frame al server Flask
                response = requests.post(SERVER_URL, files={"image": img_encoded.tobytes()})

                # Controlla lo stato della richiesta
                if response.status_code == 200:
                    # Prova ad accedere al JSON della risposta
                    try:
                        response_data = response.json()

                        # Verifica che la risposta sia un dizionario
                        if isinstance(response_data, dict):
                            # Estrai i dati dal JSON
                            face_names = response_data.get("Persona rilevata", [])
                            plate_text = response_data.get("Targa rilevata")
                            listTarghe = ["AB123CD"]
                            if plate_text in listTarghe:
                                print(f"Targa conosciuta: {plate_text}")
                            else:
                                print(f"Targa sconosciuta: {plate_text}")
                            print(f"Volti rilevati: {face_names}")
                        else:
                            print("Formato della risposta JSON inatteso:", response_data)

                    except ValueError:
                        print("Errore nel decodificare il JSON della risposta.")
                else:
                    print(f"Errore nella richiesta: Status code {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Errore nella richiesta: {e}")

        # Mostra il video in tempo reale
        cv2.imshow('Client Webcam', frame)

        # Premi 'q' per uscire
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_and_send_image()
