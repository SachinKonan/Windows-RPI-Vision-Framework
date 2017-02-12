import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import imutils
import sys
from collections import deque
import socket
import numpy as np
import time
from operator import itemgetter

# construct the argument parse and parse the arguments
# v4l2-ctl --set-ctrl brightness=130
#cmd commands:
#source ~/.profile
#workon cv
#python '/home/pi/Documents/PythonProjects/pyImage.py' or wherever u have pyImage saved

def contourArea(contours):
    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort(key=itemgetter(0))
    index = 0

    if(len(area) != 0):
        for i in range(len(area)-1,-1,-1):
            #print(area[i][0])
            if(area[i][0] < 100):
                index = i
                break
        if(area[len(area)-1][0] >=100):
            return [area[x][1] for x in range(index, len(area))]
        else:
            return [-1]
    else:
        return [-1]

def distance_to_cam(x):
    return ((10.0/12.0) * 480.0) /(2 * x * np.tan(14.8685 * np.pi/180.0)) * 12

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self.send_response(20)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:

                    if(frame != None):
                        pass
                    r, buf = cv2.imencode(".jpg", frame)
                    self.wfile.write("--jpgboundary\r\n".encode())
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                except KeyboardInterrupt:
                    break
            return

        if self.path.endswith('.html') or self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://localhost:9090/stream.mjpg" height="480px" width="640px"/>')
            self.wfile.write('</body></html>')
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        # self.stream.set(3, 1920)
        # self.stream.set(4, 1080)
        # self.stream.set(15,-100)
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


def realmain():
    global frame
    lower_green = (55, 140, 70)
    upper_green = (90, 256, 256)

    UDP_PORT = 5465
    BUFFER_SIZE = 1024
    UDP_IP = '10.140.121.108'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    font = cv2.FONT_HERSHEY_SIMPLEX

    ip = ''

    try:
        cap = WebcamVideoStream(src=0).start()
        server = ThreadedHTTPServer((ip, 9090), CamHandler)
        print("starting server")
        target = Thread(target=server.serve_forever,args=())

        i = 0
        while True:

            img = cap.read()
            t = imutils.resize(img, width=640,height=480)

            img2 = cv2.GaussianBlur(t, (5, 5), 0)
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, lower_green, upper_green)
            edged = cv2.Canny(mask, 35, 125)

            im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            indeces = contourArea(contours)

            if (indeces[0] != -1):
                cnts = [contours[i] for i in indeces]
                xmin = 1000
                ymin = 1000
                xmax = -1
                ymax = -1
                for cnt in cnts:
                    # cv2.drawContours(img, cnt, -1, (0,0,255), 3)
                    # box = cv2.boxPoints(areas)
                    # box = np.int0(box)
                    # cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
                    # print(cnt)
                    (x, y), (w, h), z = cv2.minAreaRect(cnt)
                    xmin1 = x - w / 2
                    ymin1 = y - h / 2
                    xmax1 = x + w / 2
                    ymax1 = y + h / 2
                    # cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)
                    # print(x,y)
                    # print(w, h)

                    # box = cv2.boxPoints(((x, y), (w, h), 0))
                    # box = np.int0(box)
                    # cv2.drawContours(img, [box], 0, (255, 0, 0), 2)

                    if (xmin1 < xmin):
                        xmin = xmin1
                    if (ymin1 < ymin):
                        ymin = ymin1
                    if (xmax1 > xmax):
                        xmax = xmax1
                    if (ymax1 > ymax):
                        ymax = ymax1
                        # print(x,y,w,h)


                # cv2.circle(img, (int(xmin), int(ymin)), 5, (0, 0, 255), -1)
                # cv2.circle(img, (int(xmax), int(ymax)), 5, (0, 0, 255), -1)
                width = (xmax - xmin)
                centerx = width / 2 + xmin
                height = ymax - ymin
                centery = height / 2 + ymin

                areatotal = width * height
                if (areatotal >= 1500):
                    box = cv2.boxPoints(((centerx, centery), (width, height), 0))
                    box = np.int0(box)
                    cv2.drawContours(t, [box], 0, (255, 0, 0), 2)
                    distance = distance_to_cam(height)
                    #'%s in. / %s m.' % (round(distance, 2), round(distance * 0.0254, 2))
                    #cv2.putText(t,'hello' , (10, 600),font, 3, (0, 0, 255), 3)
                    sock.sendto(('Y ' + str(centerx) + ' ' + str(centery) + ' ' + "{0:.2f}".format(distance)).encode(),(UDP_IP, UDP_PORT))
                else:
                    sock.sendto('N'.encode(), (UDP_IP, UDP_PORT))

            frame = t
            if (i == 0):
                target.start()
            i += 1

    except KeyboardInterrupt:
        cap.stop()
        target.join()
        sys.exit()

if __name__ == '__main__':
    realmain()