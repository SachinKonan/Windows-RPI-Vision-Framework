import testGearVid, visionServer
from multiprocessing import Process
import sys

if __name__ == '__main__':


    p1 = Process(target=visionServer.realmain())
    p1.start()
    p2 = Process(target=testGearVid.realmain())
    p2.start()

    