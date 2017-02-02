import serial
import time

port = '/dev/ttyUSB0'
n = 1999
N = n * 2
x = [0 for h in range(0,N)]
radarData = [0 for h in range(0,n)]
timeData = [0 for h in range(0,n)]
ser = serial.Serial(port,9600)
time.sleep(2)

if(input("Do you want to start communication?") == 'y'):
    print("Ok Im Starting Serial COmmunicatiton")
    if(ser.isOpen):
        for i in range(0,N):
            ser.write(b"a")
            x[i] = ser.readline()
    else:
        print("Serial port is not open")

samples = 0;
samples1 = 0;
for i in range(0,N):
    if(i % 2 == 0):
        radarData[samples] = float(str(x[i], 'utf-8'))* 5.0/1023.0
        samples = samples + 1
    else:
        timeData[samples1] = float(str(x[i], 'utf-8'))
        samples1 = samples1 + 1

