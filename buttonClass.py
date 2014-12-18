#class for button creation

class button(object):

	def __init__(self,color,cx,cy,w,h):
		self.color = color
		(self.cx,self.cy) = (cx,cy)
		(self.w,self.h) = (w,h)
		self.v0 = (self.cx-self.w/2,self.cy-self.h/2)
		self.v1 = (self.cx+self.w/2,self.cy+self.h/2)
		self.next = None
		self.buttonPressed = False
		self.buttonText = ""
		self.initButton()

	def initButton(self): pass

	def draw(self,canvas):
		canvas.create_rectangle(self.v0,self.v1,fill=self.color)
		canvas.create_text(self.cx,self.cy,text=self.buttonText,fill="white")

	def onMousePressed(self,event):
		if self.v0[0] <= event.x <= self.v1[0] and self.v0[1] <= event.y <= self.v1[1]:
			self.buttonPressed = True
