import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "exported_model/gesture_recognizer.task"
base_options = python.BaseOptions(model_asset_path=model_path)
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))

options = GestureRecognizerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
recognizer = GestureRecognizer.create_from_options(options)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.65,
        min_tracking_confidence=0.65)

cap = cv2.VideoCapture(0)
timestamp = 0 

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    i = 1  # left or right hand
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    np_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = frame.shape
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array)
            results = recognizer.recognize_async(mp_image, timestamp)
    
    # show the prediction on the frame
    cv2.putText(frame, results, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0,0,255), 2, cv2.LINE_AA)
    cv2.imshow('MediaPipe Hands', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    timestamp += 1
cap.release()
