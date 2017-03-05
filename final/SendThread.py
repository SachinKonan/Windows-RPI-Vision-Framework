from threading import Thread
import socket


class SendThread:
    def __init__(self, url, port):
        UDP_IP = url
        PORT = port
        self.BUFF_SIZE = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, PORT))
        self.message = ''
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=())

    def update(self):
        while True:
            if self.stopped:
                return

            self.sock.send(self.message.encode())

    def updateMessage(self,str):
        self.message = str

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
