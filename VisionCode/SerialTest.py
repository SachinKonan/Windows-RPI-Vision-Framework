import serial
import time
from threading import Thread
#port = /dev/ttyAMA0
port = 'COM3'

class SerialThread():
    def __init__(self):
        self.port = port
        self.Baud = 9600
        self.works = True
        self.stopped = False
        self.value = 0

        self.ser = serial.Serial(port,self.Baud)

        time.sleep(1)

    def start(self):
        Thread(target=self.update, args = ()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.ser.close()
                return

            if(self.ser.is_open):
                self.value = float(str(self.ser.readline(), 'utf-8'))
            else:
                self.value = -1
    def read(self):
        return self.value

    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    serialThread = SerialThread().start()

    val = serialThread.read()
    while val != -1:
        print('Distance rn is: %s '% (val))

        val = serialThread.read()
        time.sleep(0.5)

    serialThread.stop()
