import socket
from threading import Thread
import time

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
        return self

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

if __name__ == '__main__':

    receive = ReceiveThread(url='localhost',port=9090).start()

    while(True):
        print(receive.getMessage())
        time.sleep(1)