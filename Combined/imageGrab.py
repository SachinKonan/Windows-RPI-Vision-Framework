import cv2 as cv2
import time
import requests
from urllib import request
from urllib.error import  URLError

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])


url = 'http://10.140.86.216:9090/stream.mjpg'
#url = 'http://localhost:9090/stream.mjpg'
lower_green = (55, 140, 70)
upper_green = (90, 256, 256)
cap = cv2.VideoCapture(url)

while True:
    try:
        ret, img = cap.read()
        img2 = cv2.GaussianBlur(img, (5, 5), 0)
        hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_green, upper_green)
        edged = cv2.Canny(mask, 35, 125)
        cv2.namedWindow("Image w Contours")
        cv2.setMouseCallback("Image w Contours", onmouse)
        cv2.imshow('Image w Contours', mask)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    except:
        pass
cap.release()

class MjpegStream:
    def __init__(self):
        self.status = True
        self.url = 'http://localhost:9090/stream.mjpg'
        try:
            self.cap = cv2.VideoCapture(self.url)
        except RuntimeError:
            self.status=False


