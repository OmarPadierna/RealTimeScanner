#import the necessary packages
from PIL import Image
from imutils.video import VideoStream
from imutils.video import FPS
from skimage.filters import threshold_adaptive
from transform import four_point_transform
import numpy as np 
import argparse
import imutils
import time
import cv2
import pytesseract
import os

#initialize the video stream, allow the camera sensor to warmup
#and initialize the FPS counter

print("[INFO] starting video stream")
# SRC = 0 to use built in camera. 
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

#loop over the frames from the video stream


while True:
	#grab the frame from the threaded video stream and resize it
	#to have a mximum witdh of 500 px
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	#draw box on frame
	cv2.rectangle(frame, (125, 70), (375, 211),
				255, 2)
	#define box points
	coords = "[(125,70), (375,70), (375,211), (125,211)]"
	pts = np.array(eval(coords), dtype = "float32")
	cv2.imshow("Frame", frame)

	#Select only box part
	warped = four_point_transform(frame, pts)
	#convert the warped image to grayscale, then threshold it 
	#to give it that balck and whit paper peffect
	warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
	#warped = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
	#	cv2.THRESH_BINARY,11,2)
	warped = threshold_adaptive(warped,251, offset = 10)
	warped = warped.astype("uint8")*255
	#apply threshold
	#Use tesseract for OCR
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, warped)
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	print (text)
	'''
	if "kWh" in text:
		print(text)
	'''
	
	#Select consumption
	#print consumption 
	# show the output frame	
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
