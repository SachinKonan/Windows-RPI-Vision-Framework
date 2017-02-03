from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2 

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	# GET
	def do_GET(self):
		# Send response status code
		
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			
			while True:
				
				rc, img = capture.read()
				if not rc:
					pass
				r, buf = cv2.imencode(".jpg", img)
				self.wfile.write("--jpgboundary\r\n".encode())
				self.end_headers()
				self.wfile.write(bytearray(buf))
			return
		
		elif self.path.endswith('.html') or self.path == "/":
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://localhost:8081/cam.mjpg" height="240px" width="320px"/>')
			self.wfile.write('</body></html>')

def run():
	
	global capture 
	
	capture = cv2.VideoCapture(0)
	
	print('starting server...')

	# Server settings
	# Choose port 8080, for port 80, which is normally used for a http server, you need root access
	server_address = ('localhost', 8081)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()


run()
