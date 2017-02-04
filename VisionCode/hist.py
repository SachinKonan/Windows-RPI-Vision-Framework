import cv2
import numpy as np
from matplotlib import pyplot as plt

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])

lower_green = (55, 130, 20)
upper_green = (90, 256, 180)

img = cv2.imread('Target.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hist = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256] )
plt.imshow(hist,interpolation = 'nearest')
plt.show()