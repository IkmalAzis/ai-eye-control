# Import required libraries
import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import os
import time
from collections import deque

# Initialize components
cap = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

last_direction = ""
last_action_time = 0
cooldown = 2
blink_threshold = 0.015
last_blink_time = 0
blink_history = deque(maxlen=10)

# Start webcam and run detection
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            right_eye_outer = face_landmarks.landmark[33]
            right_eye_inner = face_landmarks.landmark[133]
            right_iris = face_landmarks.landmark[468]
            eye_width = right_eye_inner.x - right_eye_outer.x
            iris_pos = right_iris.x - right_eye_outer.x
            ratio = iris_pos / eye_width

            eye_height = face_landmarks.landmark[159].y - face_landmarks.landmark[145].y
            iris_y = right_iris.y - face_landmarks.landmark[145].y
            vertical_ratio = iris_y / eye_height

            direction = "CENTER"
            if ratio < 0.35:
                direction = "LEFT"
            elif ratio > 0.65:
                direction = "RIGHT"
            elif vertical_ratio < 0.35:
                direction = "UP"
            elif vertical_ratio > 0.65:
                direction = "DOWN"

            cv2.putText(frame, f"Looking: {direction}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255, 0), 2)

            top = face_landmarks.landmark[145].y
            bottom = face_landmarks.landmark[159].y
            ear = abs(top - bottom)
            current_time = time.time()

            if ear < blink_threshold:
                if (current_time - last_blink_time) > 0.3:
                    blink_history.append(current_time)
                    last_blink_time = current_time
                if len(blink_history) >= 2 and (blink_history[-1] - blink_history[-2]) < 2.5:
                    print("Double Blink Detected: Closing Tab")
                    pyautogui.hotkey('ctrl', 'w')
                    blink_history.clear()

            if direction != last_direction and (current_time - last_action_time) > cooldown:
                print(f"Looking: {direction}")
                if direction == "LEFT":
                    os.system("notepad")
                elif direction == "RIGHT":
                    webbrowser.open("https://www.google.com")
                elif direction == "UP":
                    webbrowser.open("https://www.youtube.com")
                elif direction == "DOWN":
                    os.system("control")
                last_direction = direction
                last_action_time = current_time

    cv2.imshow("Eye Control AI", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()