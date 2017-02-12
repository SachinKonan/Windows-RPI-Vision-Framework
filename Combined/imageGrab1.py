import cv2 as cv2
import time
import requests
from urllib import request
from urllib.error import  URLError
from operator import itemgetter
import numpy as np

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])

def printAreas(contours):
    area = []
    for i in range(0, len(contours)):
        area.append([cv2.contourArea(contours[i]), i])


    area.sort(key=itemgetter(0))
    index = 0
    for i in range(len(area) - 1, -1, -1):
        if (area[i][0] < 290):
            index = i
            break

    if (area[len(area) - 1][0] >= 500):
        return [area[x][1] for x in range(index, len(area))]
    else:
        return [-1]

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
        im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

        indeces = printAreas(contours)

        xmin = 1000
        ymin = 1000
        xmax = -1
        ymax = -1
        if( indeces[0] != -1):

            for i in indeces:
                cnt = contours[i]
                (x, y), (w, h), z = cv2.minAreaRect(cnt)


                xmin = x - w/2
                ymin = y - h/2

                xmax = x + w/2
                ymax = y + h/2
                cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)

                box = cv2.boxPoints(((x, y), (w, h), 0))
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
                #cv2.circle(img, (int(xmin), int(ymin)), 5, (255, 0, 0), -1)
                #cv2.circle(img, (int(xmax), int(ymax)), 5, (255, 0, 0), -1)

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
