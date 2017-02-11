import cv2
import numpy as np
from operator import itemgetter


def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])
def contourArea(contours):
    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort(key=itemgetter(1))
    index = 0
    for i in range(len(area)-1,-1,-1):
        print(area[i][0])
        if(area[i][0] < 100):
            index = i
            break

    if(area[len(area)-1][0] >=100):
        return [area[x][1] for x in range(index, len(area))]
    else:
        return [-1]

lower_green = (55, 150, 70)
upper_green = (90, 256, 256)

img = cv2.imread('Target1.png')
img = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_green, upper_green)
edged = cv2.Canny(mask, 35, 125)


im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
indeces = contourArea(contours)

if(indeces[0] != -1):
    cnts = [contours[i] for i in indeces]
    areas = [(1000,1000), (-1,-1)]
    for cnt in cnts:
        cv2.drawContours(img, cnt, -1, (0,0,255), 3)
        areas = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(areas)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
        """
        [x,y,w,h] = cv2.minAreaRect(cnt)
        if(areas[0] < x):
            areas[0] = x
        if(areas[1] < y):
            areas[1] = y
        if(areas[2] > x + w):
            areas[2] = x+w
        if(areas[3] > y+ h):
            areas[3] = y+h"""

    box = cv2.boxPoints(areas)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 0, 0), 2)


cv2.namedWindow("Image w Contours")
cv2.setMouseCallback("Image w Contours", onmouse)
cv2.imshow('Image w Contours', img)

cv2.waitKey(0)
cv2.destroyAllWindows()