import socket
from threading import Thread


class SendThread:
    def __init__(self, url='', port=8080):
        self.UDP_IP = url
        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.message = ''
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            self.sock.sendto(self.message.encode(), (self.UDP_IP, self.PORT))

    def stop(self):
        self.stopped = True

    def changeMessage(self, string):
        self.message = string

if __name__ == '__main__':
    send = SendThread('localhost', 9090).start()

    while(True):
        send.changeMessage('hello')