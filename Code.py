pip install opencv-python mediapipe pyserial


import cv2
import mediapipe as mp
import serial
import time
import math

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

        # ---- Key Points ----
        left_mouth = face[61]
        right_mouth = face[291]
        top_lip = face[13]
        bottom_lip = face[14]

        left_eye = face[159]
        right_eye = face[386]

        brow_left = face[70]
        brow_right = face[300]

        nose = face[1]

        # ---- Features ----
        mouth_width = distance(left_mouth, right_mouth)
        mouth_open = distance(top_lip, bottom_lip)
        eye_open = distance(left_eye, right_eye)

        brow_avg = (brow_left.y + brow_right.y) / 2
        brow_diff = abs(brow_left.y - brow_right.y)

        # asymmetry (for contempt)
        mouth_tilt = abs(left_mouth.y - right_mouth.y)

        # ---- Emotion Detection (Priority Order) ----

        # 1. SURPRISE
        if mouth_open > 0.06 and eye_open > 0.04:
            emotion = "SURPRISE"

        # 2. FEAR
        elif eye_open > 0.045 and mouth_open > 0.035:
            emotion = "FEAR"

        # 3. ANGER
        elif brow_avg < 0.30 and mouth_open < 0.02:
            emotion = "ANGRY"

        # 4. DISGUST (nose + lip tightening approx)
        elif mouth_open < 0.02 and mouth_width < 0.045 and brow_avg < 0.35:
            emotion = "DISGUST"

        # 5. CONTEMPT (asymmetry)
        elif mouth_tilt > 0.015:
            emotion = "CONTEMPT"

        # 6. HAPPY
        elif mouth_width > 0.06 and mouth_open < 0.03:
            emotion = "HAPPY"

        # 7. SAD
        elif mouth_width < 0.045 and mouth_open < 0.02:
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


import os

def print_dashboard(emotion, confidence, accuracy,
                    correct_predictions, total_predictions,
                    mouth_width, mouth_open, eye_open,
                    brow_avg, mouth_tilt):

    # Clear console (makes it look live)
    os.system('cls' if os.name == 'nt' else 'clear')

    print("====== AI EMOTION SYSTEM ======\n")

    print(f"Prediction : {emotion}")
    print(f"Confidence : {round(confidence, 2)}\n")

    print(f"Accuracy   : {round(accuracy, 2)}%")
    print(f"Correct    : {correct_predictions} / {total_predictions}\n")

    print("--- FEATURES ---")
    print(f"Mouth Width : {round(mouth_width, 3)}")
    print(f"Mouth Open  : {round(mouth_open, 3)}")
    print(f"Eye Open    : {round(eye_open, 3)}")
    print(f"Brow Avg    : {round(brow_avg, 3)}")
    print(f"Mouth Tilt  : {round(mouth_tilt, 3)}")

    print("\n==============================")
