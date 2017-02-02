import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

capture = None


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('.mjpg'):
            self.send_response(20)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc, img = capture.read()
                    if not rc:
                        continue
                    r, buf = cv2.imencode(".jpg", img)
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
            self.wfile.write('<img src="http://localhost:9090/cam.mjpg" height="240px" width="320px"/>')
            self.wfile.write('</body></html>')
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



def main():
    global capture

    ip = ''

    capture = cv2.VideoCapture(0)
    capture.set(3, 320)
    capture.set(4, 240)
    try:
        server = ThreadedHTTPServer((ip, 9090), CamHandler)
        print("starting server")
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

if __name__ == '__main__':
    main()
