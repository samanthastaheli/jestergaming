import cv2
import time
import pyautogui
import argparse
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from mediapipe.framework.formats import landmark_pb2

# Path to your .task model
MODEL_PATH = "exported_model/gesture_recognizer.task"

QUIT_KEY = 'q'
MOTION = "none"
M_SCORE = 0.0
ACTION = "none"
A_SCORE = 0.0

# region Async Callback Functions 

def motion_callback(result, output_image, timestamp_ms):
    """This will be called every time results are ready."""
    global MOTION, M_SCORE 
    if result.gestures:
        gesture = result.gestures[0][0]   # Top gesture
        MOTION = gesture.category_name
        M_SCORE = gesture.score
        print(f"[{timestamp_ms}] Motion Gesture: {gesture.category_name} (score={gesture.score:.2f})")


def action_callback(result, output_image, timestamp_ms):
    """This will be called every time results are ready."""
    global ACTION, A_SCORE
    if result.gestures:
        gesture = result.gestures[0][0]   # Top gesture
        ACTION = gesture.category_name
        A_SCORE = gesture.score
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
      frame = cv2.flip(frame, 1) # flip to have correct right/left sides

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


def add_frame_details(frame_display, win_x, win_y, win_w, win_h):
    h, w = frame_display.shape[:2]

    x_axis_y = h // 2
    y_axis_x = w // 2

    #Motion
    motion_text_position = (50,50)
    motion_score_position = (50,win_h-50)
    motion_color = (106,190,48)
    #Print Lines 
    cv2.line(frame_display, (0,x_axis_y), (w//2,x_axis_y), motion_color, 4) #x-axis line
    cv2.line(frame_display, (y_axis_x//2, win_y*4), (y_axis_x//2, h-(win_y*4)), motion_color, 4) #y-axis line
    #Print Motion Type
    cv2.putText(frame_display, f"Motion: {MOTION}", motion_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1,motion_color,2,cv2.LINE_AA)
    #Print Motion Score 
    cv2.putText(frame_display, f"Percent Accuracy: {M_SCORE * 100:.0f}%", motion_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1,motion_color,2,cv2.LINE_AA)


    #line to split screen
    cv2.line(frame_display, (y_axis_x,0), (y_axis_x,win_h), (255,102,178), 3) #y-axis line

    #Action
    action_text_position = (y_axis_x+50, 50)
    action_score_position = (y_axis_x+50,win_h-50)
    action_color = (255, 255, 102)
    #Print Action type
    cv2.putText(frame_display, f"Action: {ACTION}", action_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)
    #Print Action Score
    cv2.putText(frame_display, f"Percent Accuracy: {A_SCORE * 100:.0f}%", action_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)



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

            if not success:
                  break

            motion_image, action_image = split_frame(frame, hand_type)

            timestamp = int(time.time() * 1000)   # ms
            motion_recognizer.recognize_async(motion_image, timestamp)
            action_recognizer.recognize_async(action_image, timestamp)

            # Resize to correct aspect ratio 
            win_x, win_y, win_w, win_h = cv2.getWindowImageRect("Gesture Recognition")
            frame_display = resize_with_aspect_ratio(frame, win_w, win_h)

            add_frame_details(frame_display, win_x, win_y, win_w, win_h)

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