import cv2 as cv2
import time
import requests
from urllib import request
from urllib.error import  URLError
from operator import itemgetter

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])

def contourArea(contours):
    area = []
    for i in range(0, len(contours)):
        area.append([cv2.contourArea(contours[i]), i])

    area.sort(key=itemgetter(1))

    return area[len(area) - 1]

ip = '10.54.65.58'
#ip = 'localhost'
url1 = 'http://' + ip + ':5810/stream.mjpg'#url = 'http://localhost:9090/stream.mjpg'
#lower_green = (44, 1, 230)
lower_green = (70, 200, 200)
upper_green = (90, 256, 256)
cap = cv2.VideoCapture(url1)

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
        cv2.imshow('Image w Contours', img)

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


