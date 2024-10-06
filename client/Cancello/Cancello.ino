#include <Servo.h>

Servo myServo;  // Creiamo un oggetto per il servo
int servoPin = 9;  // Pin collegato al servo
int receivedData = 0;  // Variabile per memorizzare i dati ricevuti

void setup() {
  Serial.begin(9600);  // Inizializza la comunicazione seriale
  myServo.attach(servoPin);  // Collega il servo al pin specificato
  myServo.write(0);  // Porta il servo in posizione iniziale
  pinMode(13, OUTPUT);

}

void loop() {
  // Controlla se ci sono dati disponibili nella seriale
  if (Serial.available() > 0) {
    digitalWrite(13, HIGH);
    receivedData = Serial.read();  // Legge i dati dalla porta seriale

    // Se riceviamo '1', apriamo il cancello
    if (receivedData == '1') {
      apriCancello();
    }
    // Se riceviamo '0', chiudiamo il cancello
    else if (receivedData == '0') {
      chiudiCancello();
    }
  }
  else{ digitalWrite
}

void apriCancello() {
  Serial.println("Apertura del cancello...");
  myServo.write(90);  // Gira il servo in posizione aperta
}

void chiudiCancello() {
  Serial.println("Chiusura del cancello...");
  myServo.write(0);  // Gira il servo in posizione chiusa
}
