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
import socket

# construct the argument parse and parse the arguments
# v4l2-ctl --set-ctrl brightness=25
#cmd commands:
#source ~/.profile
#workon cv
#python '/home/pi/Documents/PythonProjects/pyImage.py' or wherever u have pyImage saved

def contourArea(contours):
    area = []
    for i in range(0,len(contours)):
       area.append([cv2.contourArea(contours[i]),i])

    area.sort()

    return area[len(area) - 1]

class ReceiveThread:
    def __init__(self, url = '', port = 8080):
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
            if(data.decode() != ''):
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

    ip = ''

    UDP_PORT = 8080
    UDP_RECEIVE_PORT = 8081

    UDP_COMP_IP = 'localhost'

    sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receive = ReceiveThread(UDP_COMP_IP, UDP_RECEIVE_PORT)
    receive.start()

    try:
        cap = WebcamVideoStream(src=0).start()
        server = ThreadedHTTPServer((ip, 9090), CamHandler)
        print("starting server")
        target = Thread(target=server.serve_forever,args=())

        i = 0
        while True:

            img = cap.read()
            t = imutils.resize(img, width=640,height=480)
            #frame1 = imutils.resize(img, width=600)
            #img1 = cv2.GaussianBlur(t, (5, 5), 0)

            #frame = imutils.resize(img, width=320,height=240)


            #frame1 = imutils.resize(img, width=600)
            img2 = cv2.GaussianBlur(t, (5, 5), 0)
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, lower_green, upper_green)
            edged = cv2.Canny(mask, 35, 125)

            frame = t

            string = receive.getMessage()
            if(string != ''):
                print(string)

            if (i == 0):
                target.start()
            i += 1

    except KeyboardInterrupt:
        cap.stop()
        target.join()
        sys.exit()

if __name__ == '__main__':
    realmain()
