import datetime

class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0
 
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self
 
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
 
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1
 
	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()
 
	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()
		
		
from threading import Thread
import cv2
 
class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
		
		
		def start(self):
		# start the thread to read frames from the video stream
			Thread(target=self.update, args=()).start()
			return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		
		

from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import numpy as np

def contourArea(contours):

    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort()
    if(area[len(area) - 1] >= 5 * area[0]):
        return area[len(area)-1]

    else: return 0
    
def distance_to_camera(Kwidth, focalLength, pixelWidth):
    return (Kwidth * focalLength) / pixelWidth

# construct the argument parse and parse the argumen
if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-n", "--num-frames", type=int, default=100,
		help="# of frames to loop over for FPS test")
	ap.add_argument("-d", "--display", type=int, default=-1,
		help="Whether or not frames should be displayed")
	args = vars(ap.parse_args())
	
	print("[INFO] sampling frames from webcam...")
	stream = cv2.VideoCapture(0)
	fps = FPS().start()
	lower_green = np.array([70, 50, 120])
	upper_green = np.array([120, 200, 255])
	focalLength = 341.7075686984592
	KNOWN_WIDTH = 18
	# loop over some frames
	while fps._numFrames < args["num_frames"]:
		# grab the frame from the stream and resize it to have a maximum
		# width of 400 pixels
		(grabbed, img) = stream.read()
		
		img = cv2.GaussianBlur(img, (5,5), 0)
		
		hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower_green, upper_green)
		res = cv2.bitwise_and(hsv, hsv, mask=mask)
		edged = cv2.Canny(res, 35, 125)
		im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		
		if (len(contours) > 1):
			area,place = contourArea(contours)
			
			if(area != 0):
				c = contours[place]
				M = cv2.moments(c)
				rect = cv2.minAreaRect(c)
				if (M['m00'] != 0):
					cx = int(M['m10'] / M['m00'])  # Center of MASS Coordinates
					cy = int(M['m01'] / M['m00'])
				
				if(rect[1][1] != 0):
					inches = distance_to_camera(KNOWN_WIDTH, focalLength, rect[1][1])
			
		# check to see if the frame should be displayed to our screen
		# update the FPS counter
		fps.update()
	 
	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	 
	# do a bit of cleanup
	stream.release()
	cv2.destroyAllWindows()
	
	print("[INFO] sampling THREADED frames from webcam...")
	vs = WebcamVideoStream(src=0).start()
	fps = FPS().start()
	 
	# loop over some frames...this time using the threaded stream
	while fps._numFrames < args["num_frames"]:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
	 
		# check to see if the frame should be displayed to our screen
		if args["display"] > 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
	 
		# update the FPS counter
		fps.update()
	 
	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	 
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

