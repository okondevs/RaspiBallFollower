"""
This module contain algorithms to find and
track object ( in this version is orange/red ball)

Using:
	$  python3 Tracking.py
"""

import cv2
import numpy as np
from StepMotor import StepMotor
from Servo import Servo

class Tracking:
	""" Find and track ball """

	def __init__ (self):
		""" Create type of tracker

		The best type of tracker for this project is KCF Tracker

		Other type of tracker:
		BOOSTING
		MIL
		TLD
		MEDIANFLOW
		GOTORUN -> only this used CNN (Unfortunately can't used with OpenCV 3.2 because crashes the program)

		"""
		self.tracker = cv2.TrackerKCF_create()


	def init_track_object (self, frame, objectArea):
		""" Set object which will be tracking

		Args:
			frame : frame from camera
			objectArea (rectangle): area of frame which contain object to track

		"""
		self.tracker.init(frame, boxObject)


	def tracker_update (self, frame):
		""" Update position of tracked object

		Args:
			frame: frame from camera

		"""
		return self.tracker.update(frame)



class Camera(object):
	""" Control camera """

	def __init__(self, deviceNumber):
		""" Method create camera object

		Args:
			deviceNumber (int): device number (showed after use v4l2-ctl --list-devices)

		"""
		self.cap = cv2.VideoCapture(deviceNumber)


	def set_resolution(self, width, height):
		""" Set camera width and height

		Args:
			width (int): width of frame
			height (int): height of frame

		"""
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


	def init_auto_balance(self):
		""" Method get 20 frame from camera.
		Frame at begin was too bright

		"""
		i = 20
		while(i):
		    ret, frame = self.cap.read()
		    i = i - 1


	def isOpened(self):
		""" Check activity of camera

		Return (int): true(camera is opened)/false (camera is not opened)
		"""
		return self.cap.isOpened()


	def read(self):
		""" Return frame from camera

		"""
		return self.cap.read()




if __name__ == "__main__":

	params = cv2.SimpleBlobDetector_Params()
	params.filterByArea = True
	params.minArea = 100
	params.maxArea = 99999999
	params.filterByInertia = False
	params.filterByCircularity  = False
	params.filterByConvexity  = False
	params.filterByColor = False

	detector = cv2.SimpleBlobDetector_create(params)

	cap = Camera(0)

	if cap.isOpened():
		cap.init_auto_balance()
		tracker = Tracking()
		#while(True):
		ret, frame = cap.read()
		a, b, c = cv2.split(frame)
		ret,thresh1 = cv2.threshold(c,90,255,cv2.THRESH_BINARY)
		kernel = np.ones((5,5),np.uint8)
		thresh1 = cv2.erode(thresh1,kernel,iterations = 2)
		keypoints = detector.detect(thresh1)
		#	print(keypoints[0].pt[0])
		boxObject = ( keypoints[0].pt[0]-30, keypoints[0].pt[1]-30 , 60 , 60 )
		p1 = (int(boxObject[0]), int(boxObject[1]))
		p2 = (int(boxObject[0] + boxObject[2]), int(boxObject[1] + boxObject[3]))
		tracker.init_track_object(frame, boxObject)
		cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
		cv2.imshow('frame', thresh1)
		cv2.waitKey(10)

		while(True):
			ret, frame = cap.read()
			ok, boxObject = tracker.tracker_update(frame)
			#ok, boxObject = tracker.update(frame)
			p1 = (int(boxObject[0]), int(boxObject[1]))
			p2 = (int(boxObject[0] + boxObject[2]), int(boxObject[1] + boxObject[3]))
			cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
			#print(boxObject)
			cv2.imshow('frame', frame)
			cv2.waitKey(10)
	else:
		print("Camera not opened")
