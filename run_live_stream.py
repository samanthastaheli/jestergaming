"""
Run model in live stream mode using web cam image as input.
"""

import cv2
import time
import argparse
import pyautogui
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from mediapipe.framework.formats import landmark_pb2

# Path to .task model
MODEL_PATH = "exported_model/gesture_recognizer.task"

QUIT_KEY = 'q'

# Update in callbacks
MOTION = None
ACTION = None

# region Async Callback Functions 

def motion_callback(result, output_image, timestamp_ms):
      """This will be called every time results are ready."""
      if result.gestures:
            gesture = result.gestures[0][0]   # Top gesture
            MOTION = gesture.category_name
            print(f"[{timestamp_ms}] Motion Gesture: {gesture.category_name} (score={gesture.score:.2f})")


def action_callback(result, output_image, timestamp_ms):
      """This will be called every time results are ready."""
      if result.gestures:
            gesture = result.gestures[0][0]   # Top gesture
            ACTION = gesture.category_name
            print(f"[{timestamp_ms}] Action Gesture: {gesture.category_name} (score={gesture.score:.2f})")

# endregion

# region Helper Functions

def resize_with_aspect_ratio(image, target_width, target_height):
    """
    Resize while preserving aspect ratio and adding black padding.
    """
    h, w = image.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    
    canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas


def frame_to_mp_image(frame):
      frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
      return mp_frame


def split_frame(frame, hand_type):

      _, w = frame.shape[:2]

      # Split into left and right halves
      left_half = frame[:, :w//2]
      right_half = frame[:, w//2:]
      if hand_type.lower() == "r":
            motion_image = frame_to_mp_image(left_half)
            action_image = frame_to_mp_image(right_half)
      if hand_type.lower() == "l":
            motion_image = frame_to_mp_image(left_half)
            action_image = frame_to_mp_image(right_half)

      return motion_image, action_image

# endregion

# region main

def main(hand_type):
      # Get models
      base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

      # Configure recognizer for live stream mode
      motion_options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=motion_callback,
      )
      motion_recognizer = vision.GestureRecognizer.create_from_options(motion_options)
      action_options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=action_callback,
      )
      action_recognizer = vision.GestureRecognizer.create_from_options(action_options)

      cap = cv2.VideoCapture(0)

      # Window setup
      cv2.namedWindow("Gesture Recognition", cv2.WINDOW_NORMAL)
      screen_width, screen_height = pyautogui.size()
      window_w = screen_width // 2
      window_h = int(screen_height * 0.9)
      cv2.resizeWindow("Gesture Recognition", window_w, window_h)
      cv2.moveWindow("Gesture Recognition", screen_width // 2, 0)

      timestamp = 0

      while cap.isOpened():
            success, frame = cap.read()   
            frame = cv2.flip(frame, 1) # flip to have correct right/left sides

            if not success:
                  break

            motion_image, action_image = split_frame(frame, hand_type)

            timestamp = int(time.time() * 1000)   # ms
            motion_recognizer.recognize_async(motion_image, timestamp)
            action_recognizer.recognize_async(action_image, timestamp)

            # Resize to correct aspect ratio 
            _, _, win_w, win_h = cv2.getWindowImageRect("Gesture Recognition")
            frame_display = resize_with_aspect_ratio(frame, win_w, win_h)

            # Display image in cv2 window 
            cv2.imshow("Gesture Recognition", frame_display)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord(QUIT_KEY):
                  break

      cap.release()
      motion_recognizer.close()
      action_recognizer.close()
      cv2.destroyAllWindows()


if __name__ == "__main__":
      # Argument Parser
      parser = argparse.ArgumentParser(description="Hand gesture recognizer arguments.")

      parser.add_argument(
            "--handedness",
            "-H",
            required=False,
            default="r",
            choices=['l', 'r', 'L', 'R'],
            help="'l' or 'r' handedness"
      )

      args = parser.parse_args()

      main(args.handedness)

# endregion