import os
import sys
#import pygame
import math
import time
import numpy as np
import copy

#pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
size = (width,height) = (800, 600)
eps = int(2)
textSize = 30


#screen = pygame.display.set_mode(size)
backgr = (255,255,255)
#screen.fill(backgr)
#pygame.display.flip()


class Point2D:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

	def show(self):
		return '(X:' + str(self.x) + ', Y:' + str(self.y) + ')'


class Line(Point2D):

	def __init__(self,s, e):
		self.startPos = s
		self.endPos = e
		self.color = (255,0,0)
		self.thickness = 1
		self.type = 1

	def isStartPos(self, p):
		if(p.x == self.startPos.x and p.y == self.startPos.y):
			return True
		else:
			return False

	def display(self):
		pass
		#pygame.draw.line(screen, self.color, (self.startPos.x, self.startPos.y), (self.endPos.x, self.endPos.y), self.thickness)
		#pygame.display.flip()
		
	def detect(self, mouseX, mouseY):
		slope = (self.startPos.y-self.endPos.y)/(self.startPos.x-self.endPos.x)
		slope2 = (self.startPos.y-mouseY) / (self.startPos.x-mouseX)
		if(abs(slope-slope2) < 0.3):
			if(self.startPos.x < mouseX and mouseX < self.endPos.x and self.startPos.y < mouseY and mouseY < self.endPos.y):
				return True
			else:
				return False
		else:
			return False

	
	def __repr__(self):
		return '<line>'+'<startPos>'+self.startPos.show()+'</startPos>'+'<endPos>'+self.endPos.show()+'</endPos>'+'</line>'
		#return 'Line coordinates ' + '[' + str(self.startPos.show()) + ',' + str(self.endPos.show()) + ']'
class Triangle(Line,Point2D):

	def __init__(self,a, b, c):
		self.line1 = Line(a, b)
		self.line2 = Line(b, c)
		self.line3 = Line(c, a)
		self.a = a
		self.b = b
		self.c = c
		self.startPos = a
		self.color = (255,255,0)
		self.thickness = 1
		self.type = 2

	def moveTr(self, direct, unit):
		if(direct == 'up'):
			self.line1.startPos.y -= unit
			self.line2.startPos.y -= unit
			self.line3.startPos.y -= unit
		elif(direct == 'down'):
			self.line1.startPos.y += unit
			self.line2.startPos.y += unit
			self.line3.startPos.y += unit
		elif(direct == 'left'):
			self.line1.startPos.x -= unit
			self.line2.startPos.x -= unit
			self.line3.startPos.x -= unit
		elif(direct == 'right'):
			self.line1.startPos.x += unit
			self.line2.startPos.x += unit
			self.line3.startPos.x += unit

	def isTrPoint(self, p):
		if(self.line1.isStartPos(p) or self.line2.isStartPos(p) or self.line3.isStartPos(p)):
			return True
		else:
			return False
			
	def Sameside(self, p1,p2, a,b):
		beksia = [b[0]-a[0], b[1]-a[1],0]
		p1eksia = [p1[0]-a[0],p1[1]-a[1],0]
		p2eksia = [p2[0]-a[0],p2[1]-a[1],0]
		cp1 = np.cross(beksia,p1eksia)
		cp2 = np.cross(beksia,p2eksia)
		if(np.dot(cp1,cp2) >= 0):
			return True
		else :
			return False
			
	def detect(self, mouseX, mouseY):
		if(self.Sameside((mouseX,mouseY),(self.a.x,self.a.y), (self.b.x,self.b.y),(self.c.x,self.c.y)) and self.Sameside((mouseX,mouseY),(self.b.x,self.b.y), (self.a.x,self.a.y),(self.c.x,self.c.y)) and self.Sameside((mouseX,mouseY),(self.c.x,self.c.y), (self.a.x,self.a.y),(self.b.x,self.b.y))):
			return True
		else:
			return False
		

	def display(self):
		pass
		#pygame.draw.polygon(screen, self.color, [(self.a.x,self.a.y),(self.b.x,self.b.y),(self.c.x,self.c.y)], self.thickness)
		#pygame.display.flip()
			

	def __repr__(self):
		return 'Triangle coordinates: ' + '[' + str(self.a.show()) + ',' + str(self.b.show()) + ',' + str(self.c.show()) + ']'

class Rectangle(Point2D):

	def __init__(self, p, w, h):
		self.startPos = p
		self.width = w
		self.height = h
		self.color = (0,0,255)
		self.thickness = 1
		self.type = 3

	def display(self):
		pass
		#pygame.draw.rect(screen, self.color, [self.startPos.x,self.startPos.y,self.width,self.height],self.thickness)
		#pygame.display.flip()

	def detect(self, mouseX, mouseY):
		if(self.startPos.x-eps > mouseX):
			return False
		elif(self.startPos.y-eps > mouseY):
			return False
		elif((self.startPos.y+self.height+eps) < mouseY):
			return False
		elif((self.startPos.x+self.width+eps) < mouseX):
			return False
		else :
			return True

	def __repr__(self):
		return  'Rectangle coordinates: ' + '[' + str(self.startPos.show()) + ' width:' + str(self.width) + ' height:' + str(self.height) + ' color:' + str(self.color) + ' ]'

class Square(Point2D):

	def __init__(self, p, w):
		self.startPos = p
		self.width = w
		self.height = w
		self.color=(0,255,255)
		self.thickness = 1
		self.type = 4

	def display(self):
		pass
#		pygame.draw.rect(screen, self.color, [self.startPos.x,self.startPos.y,self.width,self.height],self.thickness)
#		pygame.display.flip()
		
	def detect(self, mouseX, mouseY):
		#print "StartX:"+str(self.startPos.x)
		#print "StartY:"+str(self.startPos.y)
		#print "Height:"+str(self.height)
		#print "Width:" +str(self.width)
		#print "eps:" + str(eps)
		#print "mouseX"+str(mouseX)
		#print "mouseY"+str(mouseY)
		if(self.startPos.x-eps > mouseX):
			return False
		elif(self.startPos.y-eps > mouseY):
			return False
		elif(self.startPos.y+self.height+eps < mouseY):
			return False
		elif(self.startPos.x+self.width+eps < mouseX):
			return False
		else:
			return True

	def __repr__(self):
		return 'Square coordinates: ' + '[' + str(self.startPos.show()) + ' width:' + str(self.width) + ' height:' + str(self.height) +  ' color:' + str(self.color) + ']'

class Circle(Point2D):

	def __init__(self, c, r):
		self.startPos = c
		self.radius = r
		self.color = (255,0,255)
		self.thickness = 1
		self.type = 5

	def display(self):
		pass
		#pygame.draw.circle(screen,self.color,(self.startPos.x, self.startPos.y), self.radius,self.thickness)
		#pygame.display.flip()

	def detect(self,mouseX, mouseY):
		if math.hypot(self.startPos.x-mouseX, self.startPos.y-mouseY) <= self.radius:
			return True

		else:
			return False
	
	def __repr__(self):
		return 'Circle coordinates: ' + '[' + str(self.startPos.show()) + ' radius:' + str(self.radius) + ' color:' + str(self.color) + ' ]'
		
class Text():

	def __init__(self, string, pos):
		self.string = string
		self.startPos = pos
		self.color = BLACK
		self.font = "Comic Sans MS"
		self.size = 30
		self.type = 6
		
	def display(self):
		#myfont = pygame.font.SysFont(self.font, self.size)
		#label = myfont.render(self.string, 1, self.color)
		#screen.blit(label, (self.startPos.x, self.startPos.y))
		#pygame.display.flip()
		pass
	
	def detect(self, mouseX, mouseY):
		if(self.startPos.x > mouseX):
			return False
		elif(self.startPos.y > mouseY):
			return False
		elif(self.startPos.y+ (len(self.string)*(self.size/2)) < mouseY):
			return False
		elif(self.startPos.x+(len(self.string)*(self.size/2)) < mouseX):
			return False
		else:
			return True
		
	def __repr__(self):
		return self.string
		 


class Methods:

	def __init__(self):
		self.obj = []
		self.action = []
		self.copied = None
		self.lastAction = ''
		self.object = ''
	def displayObjects(self):
		#screen.fill(backgr)
		for singleObj in self.obj:
			#print singleObj
			if type(singleObj) is tuple:
				singleObj[0].display()
			else:
				singleObj.display()
	def addLine(self, start, end):
		startPoint = Point2D(start[0], start[1])
		endPoint = Point2D(end[0], end[1]) 
		l = Line(startPoint, endPoint)
		self.obj.append(l)
		self.displayObjects()
		return l

	def addTriangle(self,first, second, third):
		firstPoint = Point2D(first[0], first[1])
		secondPoint = Point2D(second[0], second[1])
		thirdPoint = Point2D(third[0], third[1])
		t = Triangle(firstPoint, secondPoint, thirdPoint)
		self.obj.append(t)
		self.displayObjects()
		return t

	def addRectangle(self, start, w, h):
		startPoint = Point2D(start[0], start[1])
		r = Rectangle(startPoint, w, h)
		self.obj.append(r)
		self.displayObjects()
		return r

	def addSquare(self, start, w):
		startPoint = Point2D(start[0], start[1])
		s = Square(startPoint, w)
		self.obj.append(s)
		self.displayObjects()
		return s

	def addCircle(self,center, r):
		centerPoint = Point2D(center[0], center[1])
		c = Circle(centerPoint, r)
		self.obj.append(c)
		self.displayObjects()
		return c

	def writeText(self, string, pos):
		newPos = Point2D(pos[0], pos[1])
		t = Text(string,newPos)
		self.obj.append(t)
		self.displayObjects()

	def drawImage(self, listOfPoints):
		a = []
		for i in listOfPoints:
			p = Point2D(i[0], i[1])
			a.append(p)

		self.obj.append(a)

	def delObj(self, objToDel):
		for i in self.obj:
			if(i[0] == objToDel):
				self.obj.remove(i)
				break
		self.displayObjects()

	def movePos(self, oldObj, pos):
		if(oldObj.type == 2):
			m = min(oldObj.a.y,oldObj.b.y, oldObj.c.y)
			if(m == oldObj.a.y):
				deltaX = oldObj.a.x-pos[0]
				deltaY = oldObj.a.y-pos[1]
				oldObj.startPos = oldObj.a
			elif(m == oldObj.b.y):
				deltaX = oldObj.b.x-pos[0]
				deltaY = oldObj.b.y-pos[1]
				oldObj.startPos = oldObj.b
			elif(m == oldObj.c.y):
				deltaX = oldObj.c.x-pos[0]
				deltaY = oldObj.c.y-pos[1]
				oldObj.startPos = oldObj.c
			oldObj.a.x -= deltaX
			oldObj.b.x -= deltaX
			oldObj.c.x -= deltaX
			oldObj.a.y -= deltaY
			oldObj.b.y -= deltaY
			oldObj.c.y -= deltaY
		
		else:
			#print oldObj.radius
			oldObj.startPos.x = pos[0]
			oldObj.startPos.y = pos[1]
				
	def moveObj(self, oldObj, pos):
		for (i,objLock) in self.obj:
			if(i==oldObj):
				self.movePos(i, pos)
				self.displayObjects()
				break

	def copyObj(self, obj2):
		obj = copy.deepcopy(obj2)
		self.movePos(obj, (0,0))
		self.copied = obj

	def cutObj(self, objToCut):
		for i in self.obj:
			if(i[0] == objToCut):
				copyObj = copy.deepcopy(objToCut)
				self.movePos(objToCut,(0,0))
				self.copied = objToCut
				self.obj.remove(i)
				self.displayObjects()
				return copyObj

	def pasteObj(self):
		if(self.copied is None):
			return None
		else :
			tmp = copy.deepcopy(self.copied)
			self.obj.append(tmp)
			self.displayObjects()
			self.copied = None
			return tmp

	def detectObj(self,x,y):
		for (o,objLock) in self.obj:
			if(o.detect(x,y)):
				self.object = o
				return (o,objLock)
		return None

	def changeObjColor(self,obj,color):
		for (i,objLock) in self.obj:
			if(i == obj):
				i.color = color
				if(i.thickness == 0):
					fillObjColor(obj,color)
				self.displayObjects()
				break
				
	def newPoint(self, a, b, scale):
		size = (((a.x-b.x) ** 2) + ((a.y - b.y)**2)) ** 0.5
		resize = scale*size
		newEndPosY = a.y-((resize*(a.y-b.y)) / size)
		newEndPosX = a.x-((resize*(a.x-b.x)) / size)
		return (newEndPosX, newEndPosY)
		
	def resizeObj(self,obj,scale):
		for (i,objLock) in self.obj:
			if(i == obj):
				if(i.type == 1):
					size = (((i.startPos.x-i.endPos.x) ** 2) + ((i.startPos.y - i.endPos.y)**2)) ** 0.5
					resize = scale*size
					newEndPosY = i.startPos.y- ((resize*(i.startPos.y-i.endPos.y)) / size)
					newEndPosX = i.startPos.x- ((resize*(i.startPos.x-i.endPos.x)) / size)
					ne = Point2D(newEndPosX,newEndPosY)
					i.endPos = ne
					self.displayObjects()
					break
					 
				if(i.type == 2):
					newB = self.newPoint(i.a, i.b, scale)
					newC = self.newPoint(i.a, i.c, scale)
					pointB = Point2D(newB[0], newB[1])
					pointC = Point2D(newC[0], newC[1])
					i.b = pointB
					i.c = pointC
					self.displayObjects()
					break
				
				if(i.type == 3):
					i.width *= scale
					i.height *= scale
					self.displayObjects()
					break
				if(i.type == 4):
					i.width *= scale
					i.height *= scale
					self.displayObjects()
					break
				if(i.type == 5):
					i.radius *= scale
					self.displayObjects()
					break
		return i			
		
	def changeBackgroundColor(self,color):
		global backgr
		global screen
		backgr = color
		#screen.fill(backgr)
		self.displayObjects()
		#pygame.display.flip()

	def clearPage(self):
		self.obj = []
		self.action = []
		self.copied = None
		self.lastAction = ''
		self.object = ''
		#screen.fill(backgr)
		#pygame.display.flip()
		self.displayObjects()

	def changeLineAttr(self, obj, thickness):
		for (i,objLock) in self.obj:
			if(i == obj):
				i.thickness = thickness
		self.displayObjects()

	def changeTextFont(self, obj, font):
		for (i,objLock) in self.obj:
			if(i == obj):
				i.font = font
		self.display.objects()
				
	def changeTextSize(self, obj, size):
		for (i,objLock) in self.obj:
			if(i == obj):
				i.size = size
		self.display.objects()

	def fillObjColor(self, obj, color):
		for (i,objLock) in self.obj:
			if(i == obj):
				#i.thickness = 0
				i.color = color
		self.display.objects()
