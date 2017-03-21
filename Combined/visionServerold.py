import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import imutils
import sys
import socket
import numpy as np
import time
from operator import itemgetter
import math
import os


# construct the argument parse and parse the arguments
# v4l2-ctl --set-ctrl brightness=25
# cmd commands:
# source ~/.profile
# workon cv

def contourArea(contours):
    area = []
    for i in range(0, len(contours)):
        area.append([cv2.contourArea(contours[i]), i])

    area.sort(key=itemgetter(1))

    return area[len(area) - 1]


def widthDistanceCalc(x):
    return -0.0003 * math.pow(x, 3) + 0.0881 * x * x - 10.336 * x + 553.9


class ReceiveThread:
    def __init__(self, url='', port=8080):
        UDP_IP = url
        PORT = port
        self.BUFF_SIZE = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, PORT))
        self.message = ''
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()

    def update(self):
        while True:
            if self.stopped:
                return

            data, addr = self.sock.recvfrom(self.BUFF_SIZE)
            if (data.decode() != ''):
                self.message = data.decode()
            else:
                self.message = ''

    def getMessage(self):
        return self.message

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self.send_response(20)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    r, buf = cv2.imencode(".jpg", frame)
                    try:
                        self.wfile.write("--jpgboundary\r\n".encode())
                        self.end_headers()
                        self.wfile.write(bytearray(buf))
                    except KeyboardInterrupt:
                        pass
                except KeyboardInterrupt:
                    break
            return

        if self.path.endswith('.html') or self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://localhost:5810/stream.mjpg" height="480px" width="640px"/>')
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
    global frame1

    lower_green = (55, 140, 110)
    upper_green = (90, 256, 256)

    UDP_PORT = 5800
    UDP_COMP_PORT = 5801

    UDP_IP = ''
    UDP_COMP = '10.54.65.58'

    font = cv2.FONT_HERSHEY_SIMPLEX
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receive = ReceiveThread(url=UDP_IP, port=UDP_COMP_PORT)
    receive.start()

    ip = ''
    cap = WebcamVideoStream(src=0).start()
    os.system('v4l2-ctl --set-ctrl brightness=80')

    secondcap = WebcamVideoStream(src=1).start()

    server = ThreadedHTTPServer((ip, 5810), CamHandler)
    print("starting server ")

    target = Thread(target=server.serve_forever, args=())

    try:
        i = 0
        while True:

            img = cap.read()
            img1 = secondcap.read()

            if (img == None):
                raise Exception('Cam 1 isn not Connected')
                cap.stop()
                secondcap.stop()
                target.join()
                sys.exit()
            if (img1 == None):
                raise Exception('Cam2 isn not Connected')
                sys.exit()
                cap.stop()
                secondcap.stop()
                target.join()

            t = imutils.resize(img, width=640, height=480)
            tcam2 = imutils.resize(img1, width=640, height=480)

            img2 = cv2.GaussianBlur(t, (5, 5), 0)
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, lower_green, upper_green)
            edged = cv2.Canny(mask, 35, 125)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            im2, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            if (len(cnts) >= 1):
                area, place = contourArea(cnts)

                if (area >= 100):
                    maxc = cnts[place]

                    rect = cv2.minAreaRect(maxc)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(t, [box], 0, (0, 0, 255), 2)

                    M = cv2.moments(maxc)
                    cx = int(M['m10'] / M['m00'])  # Center of MASS Coordinates
                    cy = int(M['m01'] / M['m00'])
                    rect = cv2.minAreaRect(maxc)
                    height = rect[1][0]
                    width = rect[1][1]

                    widthreal = max(width, height)
                    heightreal = min(width, height)
                    distance = widthDistanceCalc(widthreal)

                    cv2.putText(t, '%s in. ' % (round(distance, 2)), (10, 400), font, 0.5, (0, 0, 255), 1)

                    sock.sendto(('Y ' + str(cx) + ' ' + str(cy) + ' ' + "{0:.2f}".format(
                        heightreal) + ' ' + "{0:.2f}".format(widthreal)).encode(), (UDP_COMP, UDP_PORT))
            else:
                sock.sendto('N'.encode(), (UDP_COMP, UDP_PORT))

            message = receive.getMessage()

            if (message == '2'):
                frame = tcam2
            elif (message == '1'):
                frame = t
            elif (message == ''):
                frame = tcam2

            if (i == 0):
                target.start()
            i += 1

    except KeyboardInterrupt:
        cap.stop()
        secondcap.stop()
        target.join()
        sys.exit()


if __name__ == '__main__':
    realmain()
