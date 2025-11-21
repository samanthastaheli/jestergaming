import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from mediapipe.framework.formats import landmark_pb2

# Path to your .task model
MODEL_PATH = "exported_model/gesture_recognizer.task"

# This will be called every time results are ready
def gesture_callback(result, output_image, timestamp_ms):
      if result.gestures:
            gesture = result.gestures[0][0]   # Top gesture
            print(f"[{timestamp_ms}] Gesture: {gesture.category_name} (score={gesture.score:.2f})")

def main():
      mp_image = mp.Image
      base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

      # Configure recognizer for live stream mode
      options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=gesture_callback,
      )

      recognizer = vision.GestureRecognizer.create_from_options(options)

      cap = cv2.VideoCapture(0)
      timestamp = 0

      while cap.isOpened():
            success, frame = cap.read()   
            if not success:
                  break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            
            timestamp = int(time.time() * 1000)   # ms
            recognizer.recognize_async(mp_frame, timestamp)

            cv2.imshow("Gesture Recognition", frame)
            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                  break

      cap.release()
      recognizer.close()
      cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
