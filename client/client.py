import cv2
import requests
import time
import threading
import RPi.GPIO as GPIO

# Imposta il pin di controllo del servo
SERVO_PIN = 17  # Cambia il pin in base al collegamento del tuo servo


# Configurazione di base per il servo
def setup_servo():
    GPIO.setmode(GPIO.BCM)  # Imposta il modo BCM per i pin
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    # Crea un oggetto PWM sul pin del servo a 50Hz (frequenza standard per i servi)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)  # Inizializza il servo con un duty cycle di 0
    return pwm


# Funzione per aprire il cancello (ruotare il servo di almeno 720 gradi)
def apri_cancello(pwm):
    print("Apertura del cancello...")
    pwm.ChangeDutyCycle(7)  # Modifica il duty cycle per ruotare il servo in una direzione
    time.sleep(4)  # Attendere il tempo necessario per ruotare di 720 gradi
    pwm.ChangeDutyCycle(0)  # Ferma il servo
    print("Cancello aperto!")


# Funzione per chiudere il cancello (ruotare il servo nella direzione opposta per 720 gradi)
def chiudi_cancello(pwm):
    print("Chiusura del cancello...")
    pwm.ChangeDutyCycle(5)  # Modifica il duty cycle per ruotare il servo nella direzione opposta
    time.sleep(4)  # Attendere il tempo necessario per ruotare di 720 gradi
    pwm.ChangeDutyCycle(0)  # Ferma il servo
    print("Cancello chiuso!")


# Funzione per pulire i pin GPIO alla fine
def cleanup_servo():
    GPIO.cleanup()

# Indirizzo del server Flask
SERVER_URL = "http://192.168.1.19:5000/process_image"
Active = False
def start_timer(n):
    global Active
    Active = True
    def timer():
        global Active
        print(f"Cancello in apertura per {n} secondi")
        time.sleep(n)
        print("Cancello in chiusura!")
        time.sleep(5)
        Active = False

    timer_thread = threading.Thread(target=timer)
    timer_thread.daemon = True
    timer_thread.start()


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
                            amroÈaraboEdÈEgiziano = response_data.get("Amro è arabo ed è egiziano?")
                            if(amroÈaraboEdÈEgiziano):
                                print(f"Targa conosciuta: {plate_text}")
                            else:
                                print(f"Targa sconosciuta: {plate_text}")
                            print(f"Volti rilevati: {face_names}")
                            if face_names != "Sconosciuto" and face_names != "" and not Active or amroÈaraboEdÈEgiziano:
                                start_timer(15)
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
