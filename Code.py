pip install opencv-python mediapipe pyserial

import cv2
import mediapipe as mp
import serial
import time
import math

# Serial (change COM port accordingly)
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    emotion = "NONE"

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0].landmark

        # Key landmarks
        left_mouth = face[61]
        right_mouth = face[291]
        top_lip = face[13]
        bottom_lip = face[14]
        left_eye = face[159]
        right_eye = face[386]
        brow_left = face[70]
        brow_right = face[300]

        mouth_width = distance(left_mouth, right_mouth)
        mouth_open = distance(top_lip, bottom_lip)
        eye_open = distance(left_eye, right_eye)
        brow_height = (brow_left.y + brow_right.y) / 2

        # ---- Emotion Rules ----
        if mouth_width > 0.06 and mouth_open < 0.02:
            emotion = "HAPPY"

        elif mouth_open < 0.015 and brow_height < 0.3:
            emotion = "ANGRY"

        elif mouth_open > 0.05:
            emotion = "SURPRISE"

        elif eye_open > 0.04 and mouth_open > 0.03:
            emotion = "FEAR"

        elif mouth_width < 0.04 and mouth_open < 0.02:
            emotion = "SAD"

        # Send to Arduino
        arduino.write((emotion + "\n").encode())

        cv2.putText(frame, emotion, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
