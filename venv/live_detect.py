# USAGE
# python detect.py --images images

# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from math import floor
import serial
import time
debug = False
ser = serial.Serial('COM3', 57600)


def sendCommand(targetPoint):
	response = ''
	fullResponse = ''
	content = str(targetPoint)
	lenTargetPoint = len(content)
	if lenTargetPoint == 1:
		direction = '00' + content
		if debug: 
			print(direction)
	if lenTargetPoint == 2:
		direction = '0' + content
		if debug: 
			print(direction)
	if lenTargetPoint == 3:
		direction = content
		if debug: 
			print(direction)
	command = '1' + direction + '0'
	ser.flushOutput()
	ser.write((command + '\r').encode())
	response = ser.read()
	if debug:
		while response != b'\r':
			fullResponse = fullResponse + response.decode("utf-8")
			response = ser.read()
			# response = ser.read()
			if (response == b'\r'):
				print (fullResponse) 
				fullResponse = ''

def powerDown():
	ser.write(('00000' + '\r').encode())
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--images", required=True, help="path to images directory")
# args = vars(ap.parse_args())

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
imagePaths = list(paths.list_images("images"))
cap = cv2.VideoCapture(0)
var_ticks = time.time()


# for imagePath in imagePaths:
while(True):
	ret, image = cap.read()
	imageOrig = image

	print (image.shape)
	image = imutils.resize(image, width=min(400, image.shape[1]))
	# image = imutils.resize(gray, width=min(400, gray.shape[1]))
	imageOrig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = gray
	# orig = image.copy()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	# draw the original bounding boxes
	# for (x, y, w, h) in rects:
		# cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(imageOrig, (xA, yA), (xB, yB), (0, 255, 0), 2)
		if debug:
			print(xA, xB)
		midpoint = xA + ((xB - xA) / 2) 
		targetPoint = floor((midpoint / 400) * 120)
		current_time = time.time() 
		if (current_time - .3) >  var_ticks:
			if debug: 
				print(xA, xB, midpoint, targetPoint)
			sendCommand(targetPoint)

	# show some information on the number of bounding boxes
	# filename = imagePath[imagePath.rfind("/") + 1:]
	# print("[INFO] {}: {} original boxes, {} after suppression".format(
	# 	filename, len(rects), len(pick)))

	# show the output images
	# cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", imageOrig)
	# cv2.waitKey(0)
	if cv2.waitKey(20) & 0xff == ord('q'):
		break
powerDown()
cap.release()
cv2.destroyAllWindows()

