"""
Start off with test using mediapipes hand model.
"""

# import kagglehub

# Download latest version
# path = kagglehub.dataset_download("kapitanov/hagrid")

# print("Path to dataset files:", path)

# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='models/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

image = mp.Image.create_from_file("data/fist.png")

result = recognizer.recognize(image)
print(result[0][0])