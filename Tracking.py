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


	def calculate_area(self, x, y, width, height):
		""" Convert point to rectangle and calculate point to draw rectangle

		Args:
			x (float): coordinate x of detected object
			y (float): coordinate y of detected object
			width (int): width of detected object
			height (int): height of detected object

		Return:
			rectangle: which contain detected object
			p1: left top point of rectangle
			p2: right bot point of rectangle
		"""
		boxObject = ( keypoints[0].pt[0]-30, keypoints[0].pt[1]-30 , 60 , 60 )
		p1 = (int(boxObject[0]), int(boxObject[1]))
		p2 = (int(boxObject[0] + boxObject[2]), int(boxObject[1] + boxObject[3]))
		return boxObject, p1, p2


class Camera:
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


class SimpleBlobDetector:
	""" Find ball in frame. Prepare image to tracker """

	def __init__(self, **kwargs):
		""" Create object of SimpleBlobDetector with parameters

		Args:
		**kwargs:
			filterByArea (bool): filter the object based on size
			minArea (int): min size of object
			maxArea (int): max size of object
			filterByInertia (bool): all you have to know is that this measures how elongated a shape is. E.g. for a circle, this value is 1, for an ellipse it is between 0 and 1, and for a line it is 0.
			minInertiaRatio (float): min value of inertia. Remember 0 <= minInertiaRatio <= 1
			maxInertiaRatio (float): max value of inertia. Remember maxInertiaRatio <= 1
			filterByCircularity (bool): measures how close to a circle the object is.
			minCircularity (float):	min value
			maxCircularity (float): max value
			filterByConvexity (bool): please look into link, I can't describe this without image..
			minConvexity (float):	min value. Remember 0 <= minConvexity <= 1
			maxConvexity (float): max value. Remember maxConvexity <= 1

		Better description args "https://www.learnopencv.com/blob-detection-using-opencv-python-c/"
		"""
		self.params = cv2.SimpleBlobDetector_Params()
		if "filterByArea" in kwargs:
			self.params.filterByArea = kwargs['filterByArea']
		else:
			self.params.filterByArea = True
		if "minArea" in kwargs:
			self.params.minArea = kwargs['minArea']
		else:
			self.params.minArea = 100
		if "maxArea" in kwargs:
			self.params.maxArea = kwargs['maxArea']
		else:
			self.params.maxArea = 99999999
		if "filterByInertia" in kwargs:
			self.params.filterByInertia = kwargs['filterByInertia']
		else:
			self.params.filterByInertia = False
		if "minInertiaRatio" in kwargs:
			self.params.minInertiaRatio = kwargs['minInertiaRatio']
		else:
			self.params.minInertiaRatio = 0
		if "maxInertiaRatio" in kwargs:
			self.params.maxInertiaRatio = kwargs['maxInertiaRatio']
		else:
			self.params.maxInertiaRatio = 0
		if "filterByCircularity" in kwargs:
			self.params.filterByCircularity = kwargs['filterByCircularity']
		else:
			self.params.filterByCircularity  = False
		if "minCircularity" in kwargs:
			self.params.minCircularity = kwargs['minCircularity']
		else:
			self.params.minCircularity = 0
		if "maxCircularity" in kwargs:
			self.params.maxCircularity = kwargs['maxCircularity']
		else:
			self.params.maxCircularity = 0
		if "filterByConvexity" in kwargs:
			self.params.filterByConvexity = kwargs['filterByConvexity']
		else:
			self.params.filterByConvexity  = False
		if "minConvexity" in kwargs:
			self.params.minConvexity = kwargs['minConvexity']
		else:
			self.params.minConvexity = 0
		if "maxConvexity" in kwargs:
			self.params.maxConvexity = kwargs['maxConvexity']
		else:
			self.params.maxConvexity = 0

		self.params.filterByColor = False
		self.detector = cv2.SimpleBlobDetector_create(self.params)


		def detect_object(self, frame):
			""" Find object with given parameters

			Args:
				frame: image which will be analysed

			Return keypoints with detected object

			"""
			a, b, c = cv2.split(frame)
			ret,thresh1 = cv2.threshold(c,90,255,cv2.THRESH_BINARY)
			kernel = np.ones((5,5),np.uint8)
			thresh1 = cv2.erode(thresh1,kernel,iterations = 2)
			keypoints = self.detector.detect(thresh1)
			return keypoints



if __name__ == "__main__":

	cap = Camera(0)
	detector = SimpleBlobDetector()

	if cap.isOpened():
		cap.init_auto_balance()
		tracker = Tracking()
		ret, frame = cap.read()
		detector.detect_object(frame)
		boxObject, p1, p2 = tracker.calculate_area(keypoints[0].pt[0]-30, keypoints[0].pt[1]-30 , 60 , 60)
		tracker.init_track_object(frame, boxObject)
		while(True):
			ret, frame = cap.read()
			ok, boxObject = tracker.tracker_update(frame)
			p1 = (int(boxObject[0]), int(boxObject[1]))
			p2 = (int(boxObject[0] + boxObject[2]), int(boxObject[1] + boxObject[3]))
			cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
			cv2.imshow('frame', frame)
			cv2.waitKey(10)
	else:
		print("Camera not opened")
