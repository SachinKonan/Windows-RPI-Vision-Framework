import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import sys

def onmouse(k, x, y, s, p):
    global hsv
    if k == 1:  # left mouse, print pixel at x,y
        print(hsv[y, x])

def distance_to_camera(Kwidth, focalLength, pixelWidth):
    return (Kwidth * focalLength) / pixelWidth

def contourArea(contours):

    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort()
    if(area[len(area) - 1] >= 5 * area[0]):
        return area[len(area)-1]

    else: return 0

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(5, 30)
    time.sleep(2)
    cap.set(15, -8.0)

    KNOWN_WIDTH = 18

    # focalLength =  focalLength = (rect[1][1] * 74) / 18

    focalLength = 341.7075686984592

    distance_data = []

    print('press x to exit')

    counter1 = 0
    while (True):
        # Capture frame-by-frame
        ret, img = cap.read()

        length1, width1, channels = img.shape
        img = cv2.GaussianBlur(img, (5, 5), 0)

        hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)

        # lower_green = np.array([75, 200, 170])
        # lower_green = np.array([53,180,122])

        #lower_green = np.array([70, 120, 120])
        lower_green = np.array([70, 50, 120])

        upper_green = np.array([120, 200, 255])


        #upper_green = np.array([120, 200, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        res = cv2.bitwise_and(hsv, hsv, mask=mask)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        edged = cv2.Canny(res, 35, 125)

        im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        if (len(contours) > 1):

            area,place = contourArea(contours)

            print(area)
            if(area != 0):

                # print("Contxours: %d" % contours.size())
                # print("Hierarchy: %d" % hierarchy.size())

                c = contours[place]

                cv2.drawContours(img, c, -1, (0, 0, 255), 3)
                cv2.drawContours(edged,c, -1, (255, 0, 0), 3)
                perimeter = cv2.arcLength(c, True)

                M = cv2.moments(c)

                cx = 0
                cy = 0

                if (M['m00'] != 0):
                    cx = int(M['m10'] / M['m00'])  # Center of MASS Coordinates
                    cy = int(M['m01'] / M['m00'])

                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
                cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)

                cv2.line(img, (int(width1 / 2), int(length1 / 2)), (cx, cy), (255, 0, 0), 2)


                if(rect[1][1] != 0):
                    inches = distance_to_camera(KNOWN_WIDTH, focalLength, rect[1][1])

                    #print(inches)
                    distance_data.append(inches)

                counter1+=1
                #print('The len and width of the fitted rectangle are (in pixels): %s,%s' % (int(rect[1][1]), int(rect[1][0])))
                #print('Center of Mass is Approx at Location: %s,%s' % (cx, cy))

                """
                if ((cx - width1/2) >0  ):
                    print('Move to the right')
                else:
                    print('Move to the left')

                """

                """
                    im2, contours, hierarchy = cv2.findContours(s, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    edged = cv2.Canny(gray, 35, 125)

                    im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                    c = max(contours, key=cv2.contourArea)

                    rect = cv2.minAreaRect(c)
                    #cv2.drawContours(edged, contours, -1, (0, 0, 255), 3)


                    #cv2.imshow('Frame',edged)


                    if cv2.waitKey(1) & 0xFF == ord('x'):
                        break


                    # print("Contours: %d" % contours.size())
                    # print("Hierarchy: %d" % hierarchy.size())

                """


        cv2.namedWindow("Image w Contours")
        cv2.setMouseCallback("Image w Contours", onmouse)
        cv2.imshow('Image w Contours', img)

        cv2.namedWindow("HSV")
        cv2.setMouseCallback("HSV", onmouse)
        cv2.imshow('HSV', edged)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


plt.plot(distance_data)
plt.xlabel('TimeData')
plt.ylabel('Distance to Target(in) ')
plt.title('Distance vs Time From Camera')
plt.show()

