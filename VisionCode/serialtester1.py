import serial
import time

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

print('Starting Serial printing')

while True:
    port.write("Hello World")
    time.sleep(0.1)
