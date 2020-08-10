from imutils import face_utils
import imutils
import time
import cv2
import dlib
import numpy as np

def transparentOverlay(src, overlay, x, y, scale=1):
    src = src.copy()
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if y + i >= rows or x + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[y + i][x + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[y + i][x + j]
    return src

def watermarking(original, watermarked, alpha = 1, x=0, y=0):
  overlay = transparentOverlay(original, watermarked, x, y)
  output = original.copy()
  cv2.addWeighted(overlay, 1, output, 1 - 1, 0, output)
  return output

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# load glasses and mustache
glasses = cv2.imread("glasses_PNG54355.png", cv2.IMREAD_UNCHANGED)
moustache = cv2.imread("moustache-clip-art-5.png", cv2.IMREAD_UNCHANGED)

frame = cv2.imread('IMG_20190502_193227.jpg')
frame = imutils.resize(frame, height=600)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 # detect faces in the grayayscale frame
rects = detector(gray, 0)

# loopop over the face detections
for rect in rects:
    (x,y,w,h) = face_utils.rect_to_bb(rect)
    #draw face bounding box
    # cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 1)

    shape = predictor(frame, rect)
    shape = face_utils.shape_to_np(shape)
    # Draw the face landmarks on the screen.
    # # loop over the (x, y)-coordinates for the facial landmarks
    # # and draw each of them
    # for (i, (x, y)) in enumerate(shape):
    #     cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
    #     # cv2.putText(frame, str(i + 1), (x - 10, y - 10),
    #     #     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
    for (i, (x, y)) in enumerate(shape):
            if (i + 1) == 37:
                eyeLeftSide = x - 40
            if (i + 1) == 38:
                eyeTopSide = y - 30
            if (i + 1) == 46:
                eyeRightSide = x + 40
            if (i + 1) == 48:
                eyeBottomSide = y + 30

            if (i + 1) == 2:
                moustacheLeftSide = x
                moustacheTopSide = y - 10
            if (i + 1) == 16:
                moustacheRightSide = x
            if (i + 1) == 9:
                moustacheBottomSide = y

    eyesWidth= eyeRightSide - eyeLeftSide
    if eyesWidth < 0:
        eyesWidth = eyesWidth * -1
    # add glasses
    fitedGlass = imutils.resize(glasses, width=eyesWidth)

    moustacheWidth= moustacheRightSide - moustacheLeftSide
    if moustacheWidth < 0:
        moustacheWidth = moustacheWidth * -1
    # add moustache
    fitedMoustache = imutils.resize(moustache, width=moustacheWidth)
    frame = watermarking(frame, fitedGlass, x= eyeLeftSide, y= eyeTopSide)
    frame = watermarking(frame, fitedMoustache, x= moustacheLeftSide, y= moustacheTopSide)
   

# show the frame
cv2.imshow("Frame", frame)
cv2.waitKey(0)
