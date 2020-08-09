from imutils import face_utils
import imutils
import time
import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

frame = cv2.imread('IMG_20190502_101126.jpg')
frame = imutils.resize(frame, height=600)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 # detect faces in the grayayscale frame
rects = detector(gray, 0)

# loopop over the face detections
for rect in rects:
    (x,y,w,h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 1)

    shape = predictor(frame, rect)
    shape = face_utils.shape_to_np(shape)
    # Draw the face landmarks on the screen.
    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw each of them
    for (i, (x, y)) in enumerate(shape):
        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        # cv2.putText(frame, str(i + 1), (x - 10, y - 10),
        #     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

# show the frame
cv2.imshow("Frame", frame)
cv2.waitKey(0)
