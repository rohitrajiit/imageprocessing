# import the necessary packages
from PIL import Image
import pytesseract
import argparse
# import cv2
import os
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
args = vars(ap.parse_args())


text = pytesseract.image_to_string(Image.open(args['image']))

print(text)


