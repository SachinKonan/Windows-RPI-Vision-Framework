import testGearVid,testVisionServer
from threading import Thread
import time

if __name__ == '__main__':

    p1 = Thread(target= testGearVid.realmain,args=())
    p1.start()
    print('blah')

    p2 = Thread(target= testVisionServer.realmain,args=())
    p2.start()
    print('hello')

    p1.join()
    p2.join()