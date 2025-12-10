import cv2
import time
import pyautogui
import pygame
import argparse
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from mediapipe.framework.formats import landmark_pb2
from connect_w_stardew import connect_to_window, control_game, press_action, release_action, press_movement, release_movement
from motion_sm import call_motion_state
from action_sm import call_action_state

# Path to .task model
ACTION_MODEL_PATH = "exported_model_action/gesture_recognizer.task"
MOVE_MODEL_PATH = "exported_model_movement/gesture_recognizer.task"

QUIT_KEY = 'q'
START_KEY = 's'
CONTROL_KEY = 'c'
WINDOW_NAME = "Jester Gaming"

WELCOME_IMG = cv2.imread("images/welcome.png")
CONTROLS_IMG = cv2.imread("images/controls.png")

# Update in callbacks
MOTION = "none"
MOTION_DEFAULT = "none"
PREVIOUS_MOTION = "none"
M_X = 0.00
M_Y = 0.00
M_SCORE = 0.0
M_SCORE_DEFAULT = 0.0
ACTION = "none"
ACTION_DEFAULT = "none"
PREVIOUS_ACTION = "none"
A_SCORE = 0.0
A_SCORE_DEFAULT = 0.0

FRAME_INDEX = 1
FPS_Q = []


# region Async Callback Functions 

def motion_callback(result, output_image, timestamp_ms):
    """This will be called every time results are ready."""
    global MOTION, M_SCORE, M_X, M_Y 
    if result.gestures:
      gesture = result.gestures[0][0]   # Top gesture
      MOTION = gesture.category_name
      M_SCORE = gesture.score
      # print(f"[{timestamp_ms}] Motion Gesture: {gesture.category_name} (score={gesture.score:.2f})")
      if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            palm = landmarks[9]
            M_X = palm.x
            M_Y = palm.y

            # print("X: ", palm.x)
            # print("Y: ", palm.y)
    else:
        MOTION = MOTION_DEFAULT
        M_SCORE = M_SCORE_DEFAULT


def action_callback(result, output_image, timestamp_ms):
    """This will be called every time results are ready."""
    global ACTION, A_SCORE
    if result.gestures:
        gesture = result.gestures[0][0]   # Top gesture
        ACTION = gesture.category_name
        A_SCORE = gesture.score
      #   print(f"[{timestamp_ms}] Action Gesture: {gesture.category_name} (score={gesture.score:.2f})")
    else:
        ACTION = ACTION_DEFAULT
        A_SCORE = A_SCORE_DEFAULT

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

def get_models():
      """
      Get motion and action models.
      """
      # Get models
      # Configure recognizer for live stream mode
      motion_options = vision.GestureRecognizerOptions(
            base_options=python.BaseOptions(model_asset_path=MOVE_MODEL_PATH),
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=motion_callback,
      )
      motion_recognizer = vision.GestureRecognizer.create_from_options(motion_options)
      action_options = vision.GestureRecognizerOptions(
            base_options=python.BaseOptions(model_asset_path=ACTION_MODEL_PATH),
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=action_callback,
      )
      action_recognizer = vision.GestureRecognizer.create_from_options(action_options)

      return motion_recognizer, action_recognizer

# endregion

# region Screen Prints

def add_frame_details(frame_display, win_x, win_y, win_w, win_h, motion_x, motion_y):
    h, w = frame_display.shape[:2]

    x_axis_y = h // 2
    y_axis_x = w // 2

    #Motion
    motion_text_position = (50,50)
    motion_score_position = (50,win_h-75)
    motion_color = (106,190,48)
    #Print Lines 
    cv2.line(frame_display, (0,x_axis_y), (w//2,x_axis_y), motion_color, 4) #x-axis line
    cv2.line(frame_display, (y_axis_x//2, win_y*4), (y_axis_x//2, h-(win_y*4)), motion_color, 4) #y-axis line
    #Print deadzone radius
    radius = 100
    circle_y = ((win_y*4) + (h-(win_y*4)))//2
    circle_x = w//4
    cv2.circle(frame_display, (circle_x, circle_y), radius, motion_color, 4)
    #Print Motion Type
#     cv2.putText(frame_display, f"Motion: {MOTION}", motion_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1,motion_color,2,cv2.LINE_AA)
    if MOTION not in ["none", "", "run"]:
      motion_to_print = ""
      if motion_x not in ["none", ""]:
           motion_to_print = motion_to_print + motion_x + " "
      if motion_y not in ["none", ""]:
           motion_to_print = motion_to_print + motion_y
      #Print Motion Type 
      cv2.putText(frame_display, f"Motion: {motion_to_print}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, motion_color,2,cv2.LINE_AA)
      #Print Motion Score
      cv2.putText(frame_display, f"Percent Accuracy: {M_SCORE * 100:.0f}%", motion_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1,motion_color,2,cv2.LINE_AA)
    else:
      #Print Motion Type
      cv2.putText(frame_display, f"Motion: ", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, motion_color,2,cv2.LINE_AA)
      #Print Motion Score
      cv2.putText(frame_display, f"Percent Accuracy: ", motion_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1,motion_color,2,cv2.LINE_AA)

    #line to split screen
    cv2.line(frame_display, (y_axis_x,0), (y_axis_x,win_h), (255,102,178), 3) #y-axis line

    #Action
    action_text_position = (y_axis_x+50, 50)
    action_score_position = (y_axis_x+50,win_h-75)
    action_color = (255, 255, 102)
    if ACTION not in ["none", ""]:
      #Print Action type
      cv2.putText(frame_display, f"Action: {ACTION}", action_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)
      #Print Action Score
      cv2.putText(frame_display, f"Percent Accuracy: {A_SCORE * 100:.0f}%", action_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)
    else:
      #Print Action type
      cv2.putText(frame_display, f"Action: ", action_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)
      #Print Action Score
      cv2.putText(frame_display, f"Percent Accuracy: ", action_score_position, cv2.FONT_HERSHEY_SIMPLEX, 1, action_color,2,cv2.LINE_AA)

def add_motion_dot(frame_display,win_w,win_h):
      pixel_x = int(M_X * win_w)//2
      pixel_y = int(M_Y * win_h)

      if MOTION == "move":
            cv2.circle(frame_display, (pixel_x,pixel_y), 8, (255,102,178), -1)

def add_FPS(frame_display, win_w, win_h,clock):
      global FRAME_INDEX, FPS_Q
      fps_position = (0+50,win_h-25)
      fps_color = (255, 255, 102)
      #fps
      clock.tick()
      fps = int(clock.get_fps())

      cv2.putText(frame_display, f"FPS: {fps}", fps_position, cv2.FONT_HERSHEY_SIMPLEX, 1, fps_color,2,cv2.LINE_AA)

      FPS_Q.append(fps)
      FRAME_INDEX +=1

# endregion   

def play_game():
      global PREVIOUS_ACTION

      ##previous function call
      # control_game(MOTION, ACTION)

      #grab x-axis and y-axis movement inputs
      motion_x, motion_y = motion_control()

      #attempt at actionss
      if A_SCORE > 0.8:
            call_action_state(ACTION,motion_x,motion_y)
            # if PREVIOUS_ACTION != ACTION:
            #      release_action(PREVIOUS_ACTION)
            #      time.sleep(.05)
            #      press_action(ACTION)
            # PREVIOUS_ACTION = ACTION


      #state machine for motion
      #if certain action, disable motion
      if MOTION == "move":
            call_motion_state(motion_x,motion_y)
      elif ACTION in ["journal", "menu", "map"]:
            call_motion_state("none","none")
      else:
            call_motion_state("none","none")

      # press_movement(motion_x, motion_y)
      # time.sleep(.05)
      # release_movement(motion_x, motion_y)
      # PREVIOUS_MOTION = MOTION
      return motion_x,motion_y

def motion_control():
      #normalize pixel coordinates
      palm_x = M_X
      palm_y = M_Y
      center_radius = .150

      dx = palm_x - 0.5
      dy = palm_y - 0.5

      motion_x = MOTION_DEFAULT
      motion_y = MOTION_DEFAULT

      #left right
      if abs(dx) < center_radius: 
            motion_x = MOTION_DEFAULT
      else:
            motion_x = "right" if dx > 0 else "left"

      #up down
      if abs(dy) < center_radius:
            motion_y = MOTION_DEFAULT
      else:
            motion_y = "down" if dy > 0 else "up"

      return motion_x,motion_y
           
# region start up page

def display_controls_page(win_w, win_h):
      """
      Display controls image on window.
      """
      control_page = True
      while control_page:
            controls_display = resize_with_aspect_ratio(CONTROLS_IMG, win_w, win_h)
            cv2.imshow(WINDOW_NAME, controls_display)

            if cv2.waitKey(10) & 0xFF == ord(QUIT_KEY):
                  control_page = False



# endregion

# region web cam

def start_live_stream(hand_type):
      """
      Creates models and window for live connection to web cam.
      """
      # connect to the stardew game instance
      connect_to_window()

      # initialize pygame
      pygame.init()
      clock = pygame.time.Clock()

      motion_recognizer, action_recognizer = get_models()

      cap = cv2.VideoCapture(0)

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
            win_x, win_y, win_w, win_h = cv2.getWindowImageRect(WINDOW_NAME)
            frame_display = resize_with_aspect_ratio(frame, win_w, win_h)

            add_motion_dot(frame_display,win_w,win_h)
            motion_x, motion_y = play_game()
            add_frame_details(frame_display, win_x, win_y, win_w, win_h, motion_x, motion_y)
            add_FPS(frame_display,win_w,win_h,clock)

            # Display image in cv2 window 
            cv2.imshow(WINDOW_NAME, frame_display)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord(QUIT_KEY):
                  print(FPS_Q)
                  break

      cap.release()
      motion_recognizer.close()
      action_recognizer.close()

# endregion

# region main
def main(hand_type):
      start_up = True
      quit = False
      while start_up:
            # Window setup
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            screen_width, screen_height = pyautogui.size()
            window_w = screen_width // 2
            window_h = int(screen_height * 0.9)
            cv2.resizeWindow(WINDOW_NAME, window_w, window_h)
            cv2.moveWindow(WINDOW_NAME, screen_width // 2, 0)
            win_x, win_y, win_w, win_h = cv2.getWindowImageRect(WINDOW_NAME)

            # Get start image
            # img = np.zeros((window_w, window_h, 3), np.uint8) 

            # Resize to correct aspect ratio 
            welcome_display = resize_with_aspect_ratio(WELCOME_IMG, win_w, win_h)
            # center_position = (int(window_w/2), int(window_h/2))
            # cv2.putText(welcome_display, "Welcome", center_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2,cv2.LINE_AA)
            cv2.imshow(WINDOW_NAME, welcome_display)

            # Move to live stream
            key = cv2.waitKey(0) & 0xFF
            if key == ord(START_KEY):
                  start_up = False
            # Exit all windows
            if key == ord(QUIT_KEY):
                  quit = True
                  start_up = False
            if key == ord(CONTROL_KEY):
                  display_controls_page(win_w, win_h)

      if not quit:
            start_live_stream(hand_type)
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