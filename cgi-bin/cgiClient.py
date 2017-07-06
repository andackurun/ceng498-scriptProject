#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 
import socket
import sys
import methods
import json
import cPickle as pickle
import Cookie, os
#from random import randint
import time
import copy
def getMessage(conn):
	firstMessage = ''
	data = ''
	while True:
		data = conn.recv(1024)
		firstMessage += data
		if (len(firstMessage) >= 8) and (firstMessage[-8:] == "meteanda"):
			return firstMessage[:-8]			
def getIntValue(text):
	if(text != None):
		return(int(text))
	else:
		return text
def getUsername():
	cookie = Cookie.SimpleCookie()
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie.load(cookie_string)
	username = str(cookie['username'].value)
	return username
# Create instance of FieldStorage 
form = cgi.FieldStorage()
username = getUsername()

print "Content-type: text/xml"
print
print "<?xml version='1.0'?>"
print "<root>"
# Get data from fields
operation = getIntValue(form.getvalue('operationType'))
msg = form.getvalue('text')
if(msg == None):
	msg = ""

param1 = getIntValue(form.getvalue('param1'))
param2 = getIntValue(form.getvalue('param2'))
param3 = getIntValue(form.getvalue('param3'))
param4 = getIntValue(form.getvalue('param4'))
param5 = getIntValue(form.getvalue('param5'))
param6 = getIntValue(form.getvalue('param6'))

PORT  = 8008
HOST = '127.0.0.1'	# Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
drawer = methods.Methods()

#drawer.displayObjects()

if(operation == 0):
	#print "Adding New Line"
	drawer.addLine((param1,param2),(param3,param4))
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 1):
	#print "Adding New Triangle"
	drawer.addTriangle((param1,param2),(param3,param4),(param5,param6))
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 2):
	#print "Adding New Rectangle"
	drawer.addRectangle((param1,param2),param3,param4)
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 3):
	#print "Adding New Square"
	drawer.addSquare((param1,param2),param3)
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 4):
	#print "Adding New Circle"
	drawer.addCircle((param1,param2),param3)
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 5):
	timeVar = str(int(time.time())) + "Save.txt"
	serializedMessage = pickle.dumps((None,9,timeVar,username,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 6):
	#cutobj
	#print "Cutting Object"
	detectedObj = drawer.detectObj(param1,param2)
	if detectedObj is None:
		serializedMessage = pickle.dumps((None,10,None))
		s.send(serializedMessage+"end")
		#print "Object couldn't find"
	else:
		result = drawer.cutObj(detectedObj)
		#print "Object Founded"
		#print result
		serializedMessage = pickle.dumps((result,2,None))
		s.send(serializedMessage+"end")
elif(operation == 7):
	#copyobj
	detectedObj = drawer.detectObj(param1,param2)
	if detectedObj is None:
		serializedMessage = pickle.dumps((None,10,None))
		s.send(serializedMessage+"end")
	#	print "Object couldn't find"
	else:
		#print "Object copied to dashboard"
		drawer.copyObj(detectedObj)
		serializedMessage = pickle.dumps((None,10,None))
		s.send(serializedMessage+"end")
	#paste feature disabled for this phase since it requires cookies or session to store cutted or copied objects
	#We will add this feature in phase4 again.
	"""elif(operation == 8):
	#paste
	lock.acquire()
	result = drawer.pasteObj()
	if result is None:
		print "There is no object to copy"
		serializedMessage = pickle.dumps((None,10,None))
		s.send(serializedMessage+"end")
	else:
		print "Successfully pasted"
		print result
		serializedMessage = pickle.dumps((result,3,None))
		s.send(serializedMessage+"end")
	lock.release()"""
elif(operation == 9):
	drawer.clearPage()
	serializedMessage = pickle.dumps(([],4,None,None,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 10):
	#Write Text
	drawer.writeText(msg, (param1,param2))
	serializedMessage = pickle.dumps((drawer.obj[-1],1,None,username,(None,None)))
	s.send(serializedMessage+"end")
#elif(operation == 11):
	#Draw Random Image
	#TODO it needs getting mouse points etc. Logic will be determined in phase4
#	print "draw random image"
elif(operation == 12):
	#Change Object Color
	detectedObj = drawer.detectObj(param1,param2)
	if detectedObj is None:
		serializedMessage = pickle.dumps((None,10,None))
		s.send(serializedMessage+"end")
		print "Object couldn't find"
	else:
		tmp = copy.deepcopy(detectedObj)
		newColor = (param3,param4,param5)
		drawer.changeObjColor(detectedObj,newColor)
		print "Color Changed with " + str(newColor)
		serializedMessage = pickle.dumps((tmp,5,newColor))
		s.send(serializedMessage+"end")
elif(operation == 13):
	#Delete Obj
	serializedMessage = pickle.dumps((None,2,None,username,(param1,param2)))
	s.send(serializedMessage+"end")
elif(operation == 14):
	#Resize Obj
	serializedMessage = pickle.dumps((None,6,param3,username,(param1,param2)))
	s.send(serializedMessage+"end")
elif(operation == 15):
	#Change Background Color
	newColor = (param1,param2,param3)
	print "Changing Background Color to "+str(newColor)
	drawer.changeBackgroundColor(newColor)
	serializedMessage = pickle.dumps(([],7,newColor))
	s.send(serializedMessage+"end")
elif(operation == 16):
	#Move Object
	serializedMessage = pickle.dumps((None,8,(param3,param4),username,(param1,param2)))
	s.send(serializedMessage+"end")
elif(operation == 18):
	#Printing all objects
	print "Listing all objects"
	print drawer.obj
	serializedMessage = pickle.dumps((None,10,None))
	s.send(serializedMessage+"end")
elif(operation == 19):
	serializedMessage = pickle.dumps((None,10,None,None,(None,None)))
	s.send(serializedMessage+"end")
elif(operation == 20):
	serializedMessage = pickle.dumps((None,20,None,username,(param1,param2)))
	s.send(serializedMessage+"end")
responseMessage = getMessage(s)
(objList,backgroundColor,opResult) = pickle.loads(responseMessage)

drawer.obj = objList
methods.backgr = backgroundColor
for i in drawer.obj:
	print i
print "<result>"+opResult+"</result>"
print "</root>"
shutdown(s, SHUT_WR)
