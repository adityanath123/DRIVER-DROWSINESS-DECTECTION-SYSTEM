import cv2 as cv
import time
import threading
from playsound import playsound
import os

# Load the face and eye cascade classifiers
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

# Check if classifiers were loaded successfully
if face_cascade.empty() or eye_cascade.empty():
    print("Error: Failed to load Haarcascade XML files.")
    exit()

# Ensure the alarm sound file is in the same directory as the script
ALARM_SOUND = os.path.join(os.path.dirname(__file__), 'alarm.wav')

# Function to play alarm sound
def sound_alarm():
    playsound(ALARM_SOUND)

# Start video capture
video_capture = cv.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not access the camera.")
    exit()

eyes_closed_time = None  # Time when eyes first detected closed
eyes_open_time = None   # Time when eyes are detected open after the alarm
ALARM_THRESHOLD = 3  # Seconds before triggering alarm
ALARM_RESET_TIME = 7  # Seconds to wait before turning off the alarm after eyes open
alarm_on = False  # Alarm should start as False

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to read frame")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    eyes_detected = False

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))

        if len(eyes) > 0:
            eyes_detected = True
            eyes_closed_time = None  # Reset timer if eyes are open
            if alarm_on and eyes_open_time is None:
                eyes_open_time = time.time()  # Start the timer when eyes are first detected open
            alarm_on = False  # Reset alarm if eyes are open

        # Draw rectangles around face and eyes
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    # If no eyes detected, start timer
    if not eyes_detected:
        if eyes_closed_time is None:
            eyes_closed_time = time.time()  # Start timing
        elif time.time() - eyes_closed_time >= ALARM_THRESHOLD:
            if not alarm_on:
                alarm_on = True
                threading.Thread(target=sound_alarm, daemon=True).start()

    # If eyes are open and alarm was triggered, check to reset the alarm after 7 seconds
    if eyes_open_time and time.time() - eyes_open_time >= ALARM_RESET_TIME:
        alarm_on = False
        eyes_open_time = 1  # Reset after the alarm is turned off

    cv.imshow("Drowsiness Detection", frame)

    # Exit on 'q' key press
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv.destroyAllWindows()
