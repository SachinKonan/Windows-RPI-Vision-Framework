import cv2
import numpy as np
from operator import itemgetter


def onmouse(k, x, y, s, p):
    global img
    if k == 1:  # left mouse, print pixel at x,y
        print(x,y)
        #print(hsv[y, x])
def contourArea(contours):
    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort(key=itemgetter(0))
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

def distance_to_cam(x):
    return ((10.0/12.0) * 480.0) /(2 * x * np.tan(14.8685 * np.pi/180.0)) * 12

lower_green = (55, 150, 70)
upper_green = (90, 256, 256)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
img = cv2.imread('Target3.png')
img = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_green, upper_green)
edged = cv2.Canny(mask, 35, 125)


im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
indeces = contourArea(contours)

if(indeces[0] != -1):
    cnts = [contours[i] for i in indeces]
    xmin = 1000
    ymin = 1000
    xmax=-1
    ymax = -1
    z2 = 1
    for cnt in cnts:
        #cv2.drawContours(img, cnt, -1, (0,0,255), 3)
        #box = cv2.boxPoints(areas)
        #box = np.int0(box)
        #cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
        #print(cnt)
        (x,y),(w,h),z = cv2.minAreaRect(cnt)
        xmin1 = x - w/2
        ymin1 = y - h/2
        xmax1 = x + w/2
        ymax1 = y + h/2
        #cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)
        #print(x,y)
        #print(w, h)

        #box = cv2.boxPoints(((x, y), (w, h), 0))
        #box = np.int0(box)
        #cv2.drawContours(img, [box], 0, (255, 0, 0), 2)

        print('XXXXXXXX')
        if(xmin1 < xmin):
            xmin = xmin1
        if(ymin1 < ymin):
            ymin = ymin1
        if(xmax1> xmax):
            xmax = xmax1
        if(ymax1 > ymax):
            ymax = ymax1
        #print(x,y,w,h)

    print('XXXXXXXXXXXx')

    #print(xmin, ymin, xmax,ymax)

    #cv2.circle(img, (int(xmin), int(ymin)), 5, (0, 0, 255), -1)
    #cv2.circle(img, (int(xmax), int(ymax)), 5, (0, 0, 255), -1)
    width = (xmax - xmin)
    centerx = width/2 + xmin
    height = ymax - ymin
    centery = height/2 + ymin

    areatotal = width * height
    if(areatotal >= 1500):
        box = cv2.boxPoints(((centerx, centery), (width, height), 0))
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        distance = distance_to_cam(height)
        cv2.putText(img, '%s in. / %s m.' % (round(distance,2), round(distance*0.0254,2)) , (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
    else:
        pass

    cv2.namedWindow("Image w Contours")
    cv2.setMouseCallback("Image w Contours", onmouse)
    cv2.imshow('Image w Contours', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()