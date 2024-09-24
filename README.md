# SmartGate: Automated Gate Control with Face and License Plate Recognition
SmartGate is a client-server application that automates gate control by recognizing faces and license plates. When a familiar face or license plate is detected, a signal is sent to a Raspberry Pi client to open the gate by controlling a servomotor.

## Features
- Real-time face recognition using a database of known faces.
- License plate recognition using Google Cloud Vision API.
- Automated gate control: Upon recognizing a known face or license plate, the client triggers a servomotor to open the gate.
- Webcam capture: The client captures images at regular intervals and sends them to the server for processing.

## Requirements
### Client-Side (Raspberry Pi)
- Python 3.x
- OpenCV (cv2)
- Requests library (requests)
- GPIO libraries for controlling the Raspberry Pi's servomotor (RPi.GPIO or pigpio)
- A webcam connected to the Raspberry Pi
- A connected servomotor for gate control
### Server Side
- Python 3.x
- Flask
- OpenCV
- Numpy
- Face_recognition
- Google Cloud Vision API
- Google Cloud credentials file (platetextrecognition-7684c9cf2659.json)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/k0m1d3v/SmartGate.git
   cd SmartGate
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google Cloud credentials:
   - Ensure you have your GOOGLE_APPLICATION_CREDENTIALS file, and set the environment variable
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_json_file.json"
   ```
4. Add known faces:
   - Place images of known faces in the known_faces folder. Supported formats: .jpg, .png, .jpeg.
5. Set up the Raspberry Pi for GPIO control:
   - Install the necessary libraries for GPIO control (RPi.GPIO or pigpio), and ensure the servomotor is correctly connected.

## Usage
### Running the server
1. Navigate to the server directory and run:
```bash
python server.py
```

