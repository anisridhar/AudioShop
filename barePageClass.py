class barePage(object):

	#base class for all the pages in the application

	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.next = None #determines which page to go to next
		self.timerDelay = 250

	def onKeyPressed(self,event): pass
	def onMousePressed(self,event): pass
	def mouseMotion(self,event): pass
	def onTimerFired(self): pass

#passing and setting variable functions
	def passVar(self): return None
	def setVar(self,var): pass