import time
from threading import Thread
import socket


class ServerConnection:
    def __init__(self):
        self.url = 'https://google.com'
        self.host = socket.gethostbyname(self.url)
        self.connected = False
        self.marker = False
        
    def start(self):
        Thread(target= self.checkConnection, args = ()).start()
            
    def gethost(self):
        return self.host
    
    def getConnection(self):
        return self.connected
        
    def checkConnection(self):
        while True:
            
            if(self.marker):
                return 
                
            try:
                s = socket.create_connection((self.host,80),2)
                self.connected = True
            except:
                pass 
                self.connected = False
    
    def stop(self):
        self.marker = True
        
        
if __name__ == '__main__':
    connection = ServerConnection()
    connection.start()
    
    time.sleep(1)
    for i in range(0,  400):
        print(connection.getConnection())
    connection.stop()
