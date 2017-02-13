from Combined import testGearVid,testVisionServer
from multiprocessing import Barrier, Lock, Process
import time

if __name__ == '__main__':

    p1 = Process(target= testVisionServer.realmain())
    p1.start()

    print('blah')