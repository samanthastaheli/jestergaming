# !pip install --upgrade pip
# !pip install mediapipe-model-maker

"""Import the required libraries."""

# from google.colab import files
import os
import cv2

import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


#----- Load model -----#

model_path = "exported_model/gesture_recognizer.task"

options = vision.GestureRecognizerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.LIVE_STREAM,
)

recognizer = vision.GestureRecognizer.create_from_options(options)


#----- Helper Functions -----#

import cv2

# Connections between landmarks, same as mp_hands.HAND_CONNECTIONS
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

def draw_hand_landmarks(frame, hand_landmarks):
    h, w, _ = frame.shape
    # Draw points
    points = []
    for lm in hand_landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((x,y))
        cv2.circle(frame, (x,y), 4, (0,255,0), -1)
    # Draw connections
    for start_idx, end_idx in HAND_CONNECTIONS:
        cv2.line(frame, points[start_idx], points[end_idx], (0,0,255), 2)


def draw_styled_landmarks(image, results):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # Draw left hand
    mp_drawing.draw_landmarks(
        image, 
        results.left_hand_landmarks, 
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
    )

    # Draw right hand
    mp_drawing.draw_landmarks(
        image, 
        results.right_hand_landmarks, 
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    )

import numpy as np

def extract_keypoints(results):
    # Left hand
    left_hand = (
        np.array([[res.x, res.y, res.z] 
        for res in results.left_hand_landmarks.landmark]).flatten()
        if results.left_hand_landmarks else np.zeros(21 * 3)
    )

    # Right hand
    right_hand = (
        np.array([[res.x, res.y, res.z] 
        for res in results.right_hand_landmarks.landmark]).flatten()
        if results.right_hand_landmarks else np.zeros(21 * 3)
    )

    return np.concatenate([left_hand, right_hand])

def on_result(result, input_image):
    # Get OpenCV image from Mediapipe image
    np_frame = input_image.numpy_view()

    # Draw landmarks
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            draw_hand_landmarks(frame_to_show, hand_landmarks)

    # Display top gesture
    if result.gestures:
        top_gesture = result.gestures[0][0]
        label = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        cv2.putText(frame_to_show, label, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
#----- Webcam -----#

# Source - https://stackoverflow.com/q
# Posted by samuelkaris, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-20, License - CC BY-SA 4.0

sequence = []
sentence = []
predictions = []
actions = []

cap = cv2.VideoCapture(0)
# Set mediapipe model 
while cap.isOpened():

    # Read feed
    ret, frame = cap.read()

    # cv2.imshow("Webcam", frame)   # Show the frame

    # Convert frame to mediapipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # Make detections
    result = recognizer.recognize_async(mp_image)
    # top_gesture = result.gestures[0][0]
    # hand_landmarks = result.hand_landmarks
    # print(top_gesture)
    # print(hand_landmarks)

    # Convert the image to BGR format before displaying
    # image_bgr = cv2.cvtColor(mp_image.numpy_view(), cv2.COLOR_RGBA2BGR)

    # --------------------------
    # Draw prediction and landmarks
    # --------------------------
    if result.hand_landmarks:
      for hand_landmarks in result.hand_landmarks:
          draw_hand_landmarks(frame, hand_landmarks)

    # Display top gesture label
    if result.gestures:
        top_gesture = result.gestures[0][0].category_name

        cv2.putText(
            frame,
            f"Gesture: {top_gesture}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # Show frame
    cv2.imshow("Gesture Recognition", frame)

    # Break gracefully
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
