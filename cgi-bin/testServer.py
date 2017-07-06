#!/usr/bin/python

import socket
import sys
import methodsServer
import json
import cgi, cgitb
import cPickle as pickle
from threading import Thread
from threading import Lock
import time

lock = Lock()
lockBG = Lock()
lock2 = Lock()
connList = []
class Reader(Thread):
	def __init__(self, conn):
		self.conn = conn
		Thread.__init__(self)
	def getMessage(self):
		with lock2:
			firstMessage = ''
			data = ''
			while True:
				data = self.conn.recv(1024)
				if data == '':
					break
				firstMessage += data
				if (len(firstMessage) >= 3) and (firstMessage[-3:] == "end"):
					return firstMessage[:-3]
	def run(self):
		if True:
			opResult = ""
			inp = self.getMessage()
			(newObj,operation,extra,usernameFromForm,(param1,param2)) = pickle.loads(inp)
			if operation == 1 or operation == 3:
			#Adding operations with operation 1 paste operation with 3
				lockObj = Lock()
				drawer.obj.append((newObj,lockObj))
			elif operation == 2 or operation == 5 or operation == 6 or operation == 8:
				retVal = drawer.detectObj(param1,param2)
				if(retVal != None):
					detectedObj = retVal[0]
					objLock = retVal[1]
					with objLock:
						if operation == 2:
					 		drawer.delObj(detectedObj)
					 	elif operation == 5:
							drawer.changeObjColor(detectedObj,extra)
					 	elif operation == 6:
							drawer.resizeObj(detectedObj,extra)
					 	elif operation == 8:
							drawer.moveObj(detectedObj,extra)
				else:
					opResult = "Object couldn't found"
			elif operation == 4:
				drawer.clearPage()
			elif operation == 7:
			#Change Background Color
				with lockBG:
					drawer.changeBackgroundColor(extra)
			elif operation == 9:
			#save to file
				myFile = open(extra, 'w')
				objWithoutLock = []
				for i in drawer.obj:
					objWithoutLock.append(i[0])
				myFile.write(pickle.dumps((objWithoutLock,methodsServer.backgr)))
				myFile.close()
			elif operation == 10:
			#ignore it
				pass
			elif operation == 20:
				detectedObj = drawer.detectObj(param1,param2)
				print "param1:"+str(param1)+" param2:"+str(param2)+"\n"
				if detectedObj is None:
					opResult = "Object couldn't find"
				else:
					opResult = "object found"
			with lock:
				objWithoutLock = []
				for i in drawer.obj:
					objWithoutLock.append(i[0])
				conn.send(pickle.dumps((objWithoutLock,methodsServer.backgr,opResult))+"meteanda")
				print objWithoutLock
		print 'client is terminating'
		conn.close()

drawer = methodsServer.Methods()
HOST = 8008
PORT = '127.0.0.1'
#PORT = int(sys.argv[1])
if len(sys.argv) < 3:
	print "There is no load file given"
else:
	loadFile = sys.argv[2]
	with open(loadFile, 'r') as content_file:
		content = content_file.read()
		(drawer.obj,methodsServer.backgr) = pickle.loads(content)
		drawer.displayObjects()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

running = True
while running:
	conn, addr = s.accept()
	connList.append(conn)
	reader = Reader(conn)
	reader.start()
