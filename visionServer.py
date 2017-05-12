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

def procImg(img):
    frame = img

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
            self.wfile.write('<img src="http://localhost:5810/stream.mjpg" height="480px" width="640px"/>')
            self.wfile.write('</body></html>')
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class WebcamVideoStream:
    def __init__(self, src=0):

        self.stream = cv2.VideoCapture(src)

        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):

        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:

            if self.stopped:
                self.stream.release()
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


def realmain():
    global frame

    font = cv2.FONT_HERSHEY_SIMPLEX
    BUFFER_SIZE = 1024
    PORT = 5810
    ip = ''

    try:
        cap = WebcamVideoStream(src=0).start()
        server = ThreadedHTTPServer((ip, PORT), CamHandler)
        print("starting server")
        target = Thread(target=server.serve_forever,args=())

        i = 0
        while True:

            img = cap.read()

            procImg(img)
            if (i == 0):
                target.start()
            i += 1

    except KeyboardInterrupt:
        cap.stop()
        capGear.stop()
        target.join()
        sys.exit()

if __name__ == '__main__':
    realmain()
