import SimpleHTTPServer
import SocketServer as socketserver
import os
import threading

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    path_to_image = 'ok.jpg'
    img = open(path_to_image, 'rb')
    statinfo = os.stat(path_to_image)
    img_size = statinfo.st_size
    print(img_size)

def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "image/jpg")
    self.send_header("Content-length", img_size)
    self.end_headers()

def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "image/jpg")
    self.send_header("Content-length", img_size)
    self.end_headers()
    f = open(path_to_image, 'rb')
    self.wfile.write(f.read())
    f.close()

class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_adress, RequestHandlerClass):
        self.allow_reuse_address = True
        socketserver.TCPServer.__init__(self, server_adress, RequestHandlerClass, False)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = MyServer((HOST, PORT), MyHandler)
    server.server_bind()
    server.server_activate()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()