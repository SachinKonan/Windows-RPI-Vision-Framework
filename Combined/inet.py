import time
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

class InetChecker:
	def __init__(self):
		self.inet = False
		self.command = 'sudo ping -c 1 192.168.1.1'
		self.stopped = False
		
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
				
			response = Popen(self.command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().decode()
						
			if('Network is unreachable' in response):
				self.inet = False
			else:
				self.inet = True
			
			time.sleep(0.8)
			
	def getInet(self):
		return self.inet
		
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		
		
inet = InetChecker().start()

while True:
	print(inet.getInet())
	time.sleep(1)
