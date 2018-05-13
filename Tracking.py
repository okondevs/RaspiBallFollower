import cv2
import numpy as np

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 800
params.maxArea = 99999999
params.filterByInertia = False
params.filterByCircularity  = False
params.filterByConvexity  = False
params.filterByColor = False

detector = cv2.SimpleBlobDetector_create(params)
cap = cv2.VideoCapture(0)
i = 10
while(i):
    ret, frame = cap.read() #camera init
    i = i - 1
while(True):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	a, b, c = cv2.split(hsv)
	ret,thresh1 = cv2.threshold(b,120,255,cv2.THRESH_BINARY)
	kernel = np.ones((5,5),np.uint8)
	thresh1 = cv2.erode(thresh1,kernel,iterations = 2)
	keypoints = detector.detect(thresh1)
	#print(keypoints[0].pt[0])
	im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS )
	cv2.imshow('frame', im_with_keypoints)
	cv2.waitKey(10)
