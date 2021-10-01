# task4.py

# Code taken from docs.opencv.org tutorials and adapted to
# track different colors for use for Task 4 of Lab 1

import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

# Define range of color (blue - 188,50,88)
lower_color = np.array([175,80,80])
upper_color = np.array([195,255,255])

while(True):
	# Capture the fram
	ret, frame = cap.read()

	if ret:
		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Threshold the HSV image to only capture color
		mask = cv2.inRange(hsv, lower_color, upper_color)

		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(frame,frame, mask = mask)

		# Edge detection
		edges = cv2.Canny(mask,100,200)

		cv2.imshow('frame',frame)
		cv2.imshow('mask',mask)
		cv2.imshow('res',res)

		cv2.imshow('outline',edges)

		# print(frame)

		# Quit if 'q' key pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()