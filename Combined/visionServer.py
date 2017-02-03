import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import imutils
import sys

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('.mjpg'):
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
<<<<<<< HEAD
            self.wfile.write('<img src="http://localhost:8080/stream.mjpg" height="240px" width="320px"/>')
=======
            self.wfile.write('<img src="http://192.168.1.122:8000/cam.mjpg" height="240px" width="320px"/>')
>>>>>>> 6f8297ee12ea8134acc85757d2cebc098323e78c
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

    ip = '192.168.1.122'
    try:
        cap = WebcamVideoStream().start()
<<<<<<< HEAD
        server = ThreadedHTTPServer((ip, 8080), CamHandler)
=======
        server = ThreadedHTTPServer((ip, 8000), CamHandler)
>>>>>>> 6f8297ee12ea8134acc85757d2cebc098323e78c
        print("starting server")
        target = Thread(target=server.serve_forever,args=())

        i = 0
        while True:

            img = cap.read()
            img1 = imutils.resize(img, width=600)
            img2 = cv2.GaussianBlur(img1, (5, 5), 0)
            #frame = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

            frame = cv2.Canny(img, 35, 125)
            if(i == 0):
                target.start()
            i +=1

    except KeyboardInterrupt:
        raise
    except:
        
        sys.exit()

if __name__ == '__main__':
    realmain()