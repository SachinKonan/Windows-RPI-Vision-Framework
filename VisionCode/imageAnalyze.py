import cv2
import numpy as np
from matplotlib import pyplot as plt
import operator

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])
def contourArea(contours):
    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort()

    v = [[area[i+1][0]-area[i][0] for i in range(len(area)-1)]]
    index, gdiff = max(enumerate(v), key=operator.itemgetter(1))
    if(len(area) >= 2):
        if(index <= len(v) - 1):
            if(area[len(area) -1][0] >= 1300):
                return [area[len(area ) - 1], area[len(area) - 2] ]
            else:
                return 0
        else:
            return 0
    else:
        return 0

lower_green = (55, 150, 110)
upper_green = (90, 256, 180)

img = cv2.imread('Target2.png')
img = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_green, upper_green)
edged = cv2.Canny(mask, 35, 125)

"""
im2, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
result = contourArea(cnts)

if(result != 0):
    print(result)


cv2.drawContours(img, cnts, -1, (0,0,255), 3)

rect = cv2.minAreaRect(cnts[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
"""

cv2.namedWindow("Image w Contours")
cv2.setMouseCallback("Image w Contours", onmouse)
cv2.imshow('Image w Contours', edged)

cv2.waitKey(0)
cv2.destroyAllWindows()