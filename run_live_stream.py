#Code with comments
import cv2 as cv
import mediapipe as mp
import numpy as np
mpfacemesh = mp.solutions.face_mesh
FaceMesh = mpfacemesh.FaceMesh(max_num_faces=1)
mpdraw = mp.solutions.drawing_utils
drawspec1 = mpdraw.DrawingSpec(color = (255,255,0), circle_radius = 0, thickness = 1)
drawspec2 = mpdraw.DrawingSpec(color = (0,255,0), circle_radius = 0, thickness = 1)
webcam = cv.VideoCapture(0)
while True:
  
 scc,img = webcam.read()
 img = cv.flip(img,1)
 h,w,c = img.shape
 blank_img = np.zeros((h,w,c), np.uint8)
 results = FaceMesh.process(img)
 
 if results.multi_face_landmarks:
  for face_lm in results.multi_face_landmarks:
   img = blank_img
   mpdraw.draw_landmarks(img,face_lm,
         mpfacemesh.FACE_CONNECTIONS,
         drawspec1,drawspec2)
 k = cv.waitKey(1)
 if k == ord('q'):
  break
 cv.imshow('face mesh 3d', img)
webcam.release()  
cv.destroyAllWindows()