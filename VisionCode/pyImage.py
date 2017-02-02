from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import socket
from internetcheck import ServerConnection
# construct the argument parse and parse the arguments
# v4l2-ctl --set-ctrl brightness=130
#cmd commands:
#source ~/.profile
#workon cv
#python '/home/pi/Documents/PythonProjects/pyImage.py' or wherever u have pyImage saved

from threading import Thread
import cv2

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        #self.stream.set(3, 1920)
        #self.stream.set(4, 1080)
        #self.stream.set(15,-100)
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
                self.stream.release()
                return
 
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
 
    def read(self):
        # return the frame most recently read
        return self.frame
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        
        
def contourArea(contours):

    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort()
    if(area[len(area) - 1] >= 7 * area[0]):
        return area[len(area)-1]

    else: return 0
   
def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])
        
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    #lower_green = (70, 120, 120)
    #upper_green = (120, 200, 255)

    #changed from 70 to 55 for hue; hue is basically the only one that matters
    lower_green = (55, 50, 120)
    upper_green = (90, 250, 256)
    UDP_IP = '192.168.1.111'
    #UDP_IP = '10.140.123.54'
    #UDP_IP = '10.54.65.79'

    UDP_PORT = 5465
    BUFFER_SIZE = 1024
    MESSAGE1 = 'Y'
    MESSAGE2 = 'N'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    numframes = 0
    
    #connection = ServerConnection()
    #connection.start()
    time.sleep(1)
    camera = WebcamVideoStream(src=0).start()
    start_time = time.time()

    while True:
        frame = camera.read()
        # resize the frame, blur it, and convert it to the HSV
            # color space
        frame = imutils.resize(frame, width=600)
        img = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_green, upper_green)
        edged = cv2.Canny(mask, 35, 125)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        im2, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        if(numframes == 0): print(img.shape)
        
        
        if (len(cnts) > 1):
            area,place = contourArea(cnts)
            if(area != 0):
                c = cnts[place]
                #cv2.drawContours(frame, c, -1, (0, 0, 255), 3)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])  # Center of MASS Coordinates
                cy = int(M['m01'] / M['m00'])
                rect = cv2.minAreaRect(c)
                length = rect[1][1]
                
                sock.sendto(('Y ' + str(cx) + ' ' + str(cy) + ' '+ "{0:.2f}".format(length)).encode(),(UDP_IP,UDP_PORT))
                #sock.sendto(('Y').encode(),(UDP_IP,UDP_PORT))
        else:
             sock.sendto('N'.encode(),(UDP_IP,UDP_PORT))
        
        """
        cv2.namedWindow("Image w Contours")
        cv2.setMouseCallback("Image w Contours", onmouse)
        cv2.imshow('Image w Contours', frame)
        key = cv2.waitKey(1) & 0xFF
        
        
        
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
        #if(numframes == 0): print(frame.shape)
        """
        numframes+=1
        
        if numframes >= 200:
            break
            
    
    camera.stop()
    totTime = time.time() - start_time
    
    print("--- %s seconds ---" % (totTime))
    
    print('----%s fps ----' % (numframes / totTime))
    
    print(numframes)
    # cleanup the camera and close any open windows
    
    cv2.destroyAllWindows()
    #connection.stop()
    
    #sock.sendto('D'.encode(),(UDP_IP,UDP_PORT))


