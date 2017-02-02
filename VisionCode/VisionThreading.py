import cv2
import numpy as np
import socket
import time
import threading
import Queue

print##lower_range = np.array([160,200,119])
##upper_range = np.array([180,255,255])
lower_range = np.array([47,150, 37])
upper_range = np.array([85,255,255])


widthMin = 100
heightMin = 0
widthmax = 10000
heightmax = 10000
tempString = "0000"

UDP_IP = "10.8.42.2"
UDP_PORT = 8420

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

class frameThread(threading.Thread):
    def __init__(self, threadID, name, multiImageQ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.multiImageQ = multiImageQ
    
    def run(self):
        print("Starting " + self.name)
        grabFrames()
        print( "Ending " + self.name)

class filterThread (threading.Thread):
    def __init__(self, threadID, name, multiImageQ, multiImageQ2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.multiImageQ = multiImageQ
        self.multiImageQ2 = multiImageQ2
    
    def run(self):
        print( "Starting " + self.name)
        filterFrame()
        print( "Ending " + self.name)

class contourThread(threading.Thread):
    def __init__(self, threadID, name, multiImageQ2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.multiImageQ2 = multiImageQ
    
    def run(self):
        print( "Starting " + self.name)
        filterContours()
        print ("Ending " + self.name)

class MultiImage(object):
    hsv = None
    time = None
    frame = None

def grabFrames():
    while True:
        try:
            capIndex = 0
            while True:
                try:
                    cap = cv2.VideoCapture(capIndex)
                    if cap.isOpened():
                        break
                    cap.release()
                    capIndex = (capIndex + 1) % 20
                except:
                    pass 
            cap.set(3, 1920)
            cap.set(4, 1080)
            cap.set(5, 30)
            time.sleep(2)
            cap.set(15, -8.0)
            failCount = 0
            savecount = 0
            while(True):
                multiImage = MultiImage()
                ret, frame = cap.read()
                if ret == True:
                    time3 = int(round(time.time() * 1000))
                    multiImage.time = time3
                    multiImage.frame = frame
                    multiImageQ.put(multiImage)
                    #cv2.imwrite('/tmp/image.jpg',frame)
                    savecount += 1
                    if savecount > 100:
                        cv2.imwrite('/tmp/image.jpg',frame)
                        savecount = 0
                else:
                    failCount += 1
                    if failCount > 20:
                        break
            cap.release()
        except:
            pass
def filterFrame():
    while True:
        try:
            if not multiImageQ.empty():
                while (multiImageQ.qsize() > 0): #grab most recent frame
                    multiImage = multiImageQ.get()
                frame = multiImage.frame
                hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV) #Allows filtering in hsv
                multiImage.hsv = hsv
                multiImageQ2.put(multiImage)
        except:
            pass

def filterContours():
    while (True):
        try:
            largestA = 0
            largestC = None
            
            multiImage = multiImageQ2.get()
            
            while (multiImageQ2.qsize() > 0):
                multiImage = multiImageQ2.get()
            
            time1 = multiImage.time
            hsv = multiImage.hsv
            frame = multiImage.frame
            mask = cv2.inRange(hsv, lower_range, upper_range) #Filters
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
            
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                width = w
                height = h
                    #pt1 = x,y
                    #pt2 = x + w, y + h
                    #cv2.rectangle(frame, pt1, pt2, (0,255,0), 4)
                if (width<widthmax) and (height<heightmax) and (width >= widthMin) and (height > heightMin):
                    currentArea = cv2.contourArea(cnt)
                    if (largestA < currentArea):
                        largestC = cnt
                        largestA = currentArea
            if (largestC != None):
                Lx,Ly,Lw,Lh = cv2.boundingRect(largestC)
                pt1 = Lx,Ly
                pt2 = Lx + Lw, Ly +Lh
                cv2.rectangle(frame, pt1, pt2, (0,255,0), 4)
                centerX = (tempString+str((Lx+(Lw/2))))[-4:]
                centerY = (tempString+str((Ly+(Lh/2))))[-4:]

		H = (tempString+str(hsv[centerY, centerX][0]))[-3:]
		S = (tempString+str(hsv[centerY, centerX][1]))[-3:]
		V = (tempString+str(hsv[centerY, centerX][2]))[-3:]

                print centerX,
                print centerY
                #print "hi",
                #print time1
                currentTime = int(round(time.time() * 1000))
                sock.sendto(centerX + centerY + H + S + V , (UDP_IP, UDP_PORT))
                #print str(currentTime - time1) + " " +  centerX
                cv2.drawContours(mask, [largestC], 0, (0,255,0), 3)
            else:
                centerY = "0000"
                centerX = "0000"
		H = "000"
		S = "000"
		V = "000"
                print centerX,
                print centerY
                #print time1
                currentTime = int(round(time.time() * 1000))
                sock.sendto(centerX + centerY + H + S + V, (UDP_IP, UDP_PORT))
                #print currentTime - time1
            try:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                pass
        except:
            pass

#frameQ = Queue.Queue(0)
#timeQ = Queue.Queue(0)
#time2Q = Queue.Queue(0)
#frame2Q = Queue.Queue(0)
#hsvQ = Queue.Queue(0)
multiImageQ = Queue.Queue(0)
multiImageQ2 = Queue.Queue(0)
lock = threading.Lock()
thread1 = frameThread(0, "Thread-1", 0)
thread2 = filterThread(0, "Thread-2", 0,0)
thread3 = contourThread(0, "Thread-3", 0)

thread1.daemon=True
thread2.daemon=True
thread3.daemon=True

#thread1.start()
thread2.start()
thread3.start()

grabFrames()
