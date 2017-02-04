import cv2 as cv2
import time
import requests
import urllib
def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])


url = 'http://localhost:9090/stream.mjpg'
cap = cv2.VideoCapture(url)

while True:
    try:
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        cv2.namedWindow("Image w Contours")
        cv2.setMouseCallback("Image w Contours", onmouse)
        cv2.imshow('Image w Contours', hsv)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    except:
        break
cap.release()